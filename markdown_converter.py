from pathlib import Path
import os, sys, subprocess, shutil, re, unicodedata
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from markdownify import markdownify as md_from_html

ROOT = Path(__file__).resolve().parent
EXPORTS = ROOT / "exports"            # input .doc / .docx
EXPORTS_DOCX = ROOT / "exports_docx"  # generated .docx
DOCS = ROOT / "docs"                  # output .md
ASSETS = DOCS / "assets"

LO = os.environ.get("LIBREOFFICE_EXE",
    r"C:\Program Files\LibreOffice\program\soffice.exe")

def msg(s): print(s, flush=True)
def sh(cmd): msg("+ " + " ".join(map(str, cmd))); return subprocess.run(cmd, check=True)

def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+","-", s).strip("-").lower()
    return s or "page"

def ensure_dirs():
    for d in (EXPORTS, EXPORTS_DOCX, DOCS, ASSETS):
        d.mkdir(parents=True, exist_ok=True)

def maybe_convert_doc_to_docx():
    docs = sorted(EXPORTS.glob("*.doc"))
    if not docs:
        msg("No .doc files found → skipping .doc → .docx.")
        return
    if not Path(LO).exists():
        msg(f"LibreOffice not found at {LO} → skipping .doc → .docx. "
            "Put .docx in exports/ or install LibreOffice.")
        return
    sh([LO, "--headless", "--nologo", "--nodefault", "--nolockcheck", "--norestore",
        "--convert-to", 'docx:MS Word 2007 XML', "--outdir", str(EXPORTS_DOCX), *map(str, docs)])

def rewrite_img_links(md_text: str, slug_base: str, names: set[str]) -> str:
    # Only rewrite bare filenames that were actually saved as attachments
    def repl(m):
        alt, url = m.group(1), m.group(2)
        name = Path(url).name
        if name in names and ("/" not in url and "\\" not in url):
            return f"![{alt}](assets/{slug_base}/{name})"
        return m.group(0)
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl, md_text)

def docx_to_md_markitdown():
    from markitdown import MarkItDown
    # build input set
    docx_files = sorted(list(EXPORTS_DOCX.glob("*.docx")) + list(EXPORTS.glob("*.docx")))
    if not docx_files:
        sys.exit("No .docx found in exports_docx/ or exports/. "
                 "Add .docx or enable LibreOffice conversion.")
    mdx = MarkItDown()
    for f in docx_files:
        base = slug(f.stem)
        out_md = DOCS / f"{base}.md"
        dest_dir = ASSETS / base
        dest_dir.mkdir(parents=True, exist_ok=True)

        res = mdx.convert(str(f))

        # Save attachments (if any)
        names = set()
        if getattr(res, "attachments", None):
            for name, data in res.attachments.items():
                (dest_dir / name).write_bytes(data)
                names.add(name)

        # Rewrite image links in the markdown
        md_text = rewrite_img_links(res.text_content, base, names)
        out_md.write_text(md_text, encoding="utf-8")
        msg(f"Wrote {out_md} (+ {len(names)} image(s))")

def is_mhtml(p: Path) -> bool:
    try:
        head = p.open("rb").read(4096).decode("utf-8", "ignore")
        return "Content-Type: multipart/related" in head or "Content-Location:" in head
    except Exception:
        return False

def mhtml_to_markdown(src_path: Path, out_md: Path, assets_dir: Path):
    # Parse the MHTML “email”
    with src_path.open("rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # find the HTML part
    html_text = None
    cid_map = {}
    parts = [msg] + list(msg.walk())
    for part in parts:
        if part.get_content_type() == "text/html" and html_text is None:
            html_text = part.get_content()
        # save inline parts (images, etc.)
        fn = part.get_filename()
        if fn or part.get_content_maintype() in {"image", "audio", "video"}:
            data = part.get_content()
            assets_dir.mkdir(parents=True, exist_ok=True)
            name = Path(fn or f"part-{len(cid_map)}").name
            (assets_dir / name).write_bytes(data)
            cid = part.get("Content-ID")
            if cid:
                cid_map[cid.strip("<>")] = name
            loc = part.get("Content-Location")
            if loc:
                cid_map[loc] = name   # handle Content-Location references too

    if html_text is None:
        raise SystemExit(f"No HTML part in {src_path}")

    soup = BeautifulSoup(html_text, "lxml")

    # rewrite src=cid:… and src by Content-Location to local assets
    rel_assets = assets_dir.relative_to(DOCS).as_posix()
    for tag in soup.find_all(src=True):
        src_attr = tag["src"]
        if src_attr.startswith("cid:"):
            key = src_attr[4:]
            if key in cid_map:
                tag["src"] = f"{rel_assets}/{cid_map[key]}"
        elif src_attr in cid_map:  # direct Content-Location
            tag["src"] = f"{rel_assets}/{cid_map[src_attr]}"

    for img in soup.find_all("img"):
        if "alt" not in img.attrs:
            img["alt"] = ""

    md_text = md_from_html(str(soup), heading_style="ATX")

    # rewrite bare image links like ![](image.png) to assets/<slug>/image.png
    def fix_md_images(text: str, page_slug: str):
        def repl(m):
            alt, url = m.group(1), m.group(2)
            if "/" not in url and "\\" not in url:
                return f"![{alt}](assets/{page_slug}/{url})"
            return m.group(0)
        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl, text)

    md_text = fix_md_images(md_text, assets_dir.name)
    out_md.write_text(md_text, encoding="utf-8")
    print(f"[MHTML] {src_path.name} -> {out_md.relative_to(ROOT)}")

def convert_sources():
    DOCS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    # 1) Handle MHTML-like .doc files directly
    for p in sorted(EXPORTS.glob("*.doc")):
        if is_mhtml(p):
            base = slug(p.stem)
            mhtml_to_markdown(
                p,
                DOCS / f"{base}.md",
                ASSETS / base
            )
            print(f"[MHTML] -> {DOCS / (base + '.md')}")
        else:
            # fallback: keep your LibreOffice path to docx then process docx
            pass

    # 2) Also handle any real .docx via MarkItDown (unchanged)
    from markitdown import MarkItDown
    mdx = MarkItDown()
    docx_files = sorted(list(EXPORTS_DOCX.glob("*.docx")) + list(EXPORTS.glob("*.docx")))
    for f in docx_files:
        base = slug(f.stem)
        res = mdx.convert(str(f))
        (DOCS / f"{base}.md").write_text(res.text_content, encoding="utf-8")
        if getattr(res, "attachments", None):
            dst = ASSETS / base
            dst.mkdir(parents=True, exist_ok=True)
            for name, data in res.attachments.items():
                (dst / name).write_bytes(data)
        print(f"[DOCX]  -> {DOCS / (base + '.md')}")

def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    # Convert all .doc that are actually MHTML
    handled = False
    for doc in sorted(EXPORTS.glob("*.doc")):
        if is_mhtml(doc):
            base = slug(doc.stem)
            mhtml_to_markdown(doc, DOCS / f"{base}.md", ASSETS / base)
            handled = True

    # (Optional) Also convert any real .docx via MarkItDown if you have them
    docx_files = sorted(EXPORTS.glob("*.docx"))
    if docx_files:
        from markitdown import MarkItDown
        mdx = MarkItDown()
        for f in docx_files:
            base = slug(f.stem)
            res = mdx.convert(str(f))
            (DOCS / f"{base}.md").write_text(res.text_content, encoding="utf-8")
            if getattr(res, "attachments", None):
                d = ASSETS / base; d.mkdir(parents=True, exist_ok=True)
                for name, data in res.attachments.items():
                    (d / name).write_bytes(data)
            print(f"[DOCX]  {f.name} -> docs/{base}.md")

    if not handled and not docx_files:
        sys.exit("No convertible inputs found in exports/ (.doc as MHTML or .docx).")

if __name__ == "__main__":
    main()