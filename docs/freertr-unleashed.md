Freertr - Unleashed



# Freertr - Unleashed

# References

[1] <http://docs.freertr.org/guides/getting-started/003-unleash/>

[2] <https://unix.stackexchange.com/questions/152331/how-can-i-create-a-virtual-ethernet-interface-on-a-machine-without-a-physical-ad>

[3] <https://askubuntu.com/questions/1004388/sysctl-permission-denied>

Tutorial

## 2 Installation[¶](http://docs.freertr.org/guides/getting-started/003-unleash/#2-installation)

### 2.1 Pre-requisites[¶](http://docs.freertr.org/guides/getting-started/003-unleash/#21-pre-requisites)

In order to illustrate this binding operation, I've added one new interfaces to my VirtualBox Debian guest OS.

```
sudo lsmod | grep dummy
sudo modprobe dummy
sudo lsmod | grep dummy
dummy                  16384  0
sudo ip link add enp0s9 type dummy
```

run ip a

```
ip a
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether fa:16:3e:24:34:d8 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.55.2.161/24 metric 100 brd 10.55.2.255 scope global dynamic ens3
       valid_lft 85276sec preferred_lft 85276sec
    inet6 fe80::f816:3eff:fe24:34d8/64 scope link 
       valid_lft forever preferred_lft forever
```

As this interface is totally controlled by freeRtr we need to reset it:

```
ip addr flush dev enp0s9
```

In order to avoid future problem (disable TCP-offload)

```
cat <<EOF | sudo tee /root/tcp-offload-off.sh

#! /bin/bash

/sbin/ethtool -K \$1 rx off
/sbin/ethtool -K \$1 tx off
/sbin/ethtool -K \$1 sg off
/sbin/ethtool -K \$1 tso off
/sbin/ethtool -K \$1 ufo off
/sbin/ethtool -K \$1 gso off
/sbin/ethtool -K \$1 gro off
/sbin/ethtool -K \$1 lro off
/sbin/ethtool -K \$1 rxvlan off
/sbin/ethtool -K \$1 txvlan off
/sbin/ethtool -K \$1 ntuple off
/sbin/ethtool -K \$1 rxhash off

EOF
```

```
sudo chmod u+x /root/tcp-offload-off.sh
```

```
sudo /root/tcp-offload-off.sh enp0s9
```

**Result**

```
sudo /root/tcp-offload-off.sh enp0s9
Actual changes:
tx-checksum-ip-generic: off
tx-tcp-segmentation: off [not requested]
tx-tcp-ecn-segmentation: off [not requested]
tx-tcp-mangleid-segmentation: off [not requested]
tx-tcp6-segmentation: off [not requested]
Actual changes:
tx-scatter-gather: off
tx-scatter-gather-fraglist: off
tx-generic-segmentation: off [not requested]
Could not change any device features
```

Enable promiscuous mode and set MTU to 8192 as freeRtr is able to handle jumbo frames

```
sudo ip link set enp0s9 up promisc on mtu 8192
```

Enable `enp0s9`

```
sudo ip link set enp0s9 up
```

IPv6 will be handled by freeRtr, therefore we disable IPv6 from Linux perspective

```
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.route.flush=1
```

## FreeRouter S/w

Let's add an additional interface definition `eth3`

* `eth3`, A-end:`127.0.0.1 1003` ---- B-end:`127.0.0.1 5003`

In this example B-end will be stitched to an existing Linux interface. `r1@eth3` which has socket `127.0.0.1 1003` will be bind to `enp0s9` Linux interface. In order to accomplish this, we will use a simple tool called `pcapInt` part of freeRtr bundles

Let's first install freeRtr addtional tools bundle.

```
sudo mkdir /rtr
cd /rtr
wget http://www.freertr.net/rtr.jar
```

install Dependencies

```
sudo apt-get install --no-install-recommends --no-install-suggests --yes default-jre-headless
```

These tools are basically tools used to ensure freeRtr packet forwarding in different context and dataplane.

```
~/rtr$ ls -ltrh *.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 vlan.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 ttyLin.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 tapInt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 stdLin.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 sender.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 rawInt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 ptyRun.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 pcapInt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 pcap2pcap.bin
-rwxr-xr-x 1 dcollin5 dcollin5  27K Dec 31  2009 p4xdp_user.bin
-rw-r--r-- 1 dcollin5 dcollin5 1.3K Dec 31  2009 p4xdp_pass.bin
-rw-r--r-- 1 dcollin5 dcollin5 101K Dec 31  2009 p4xdp_kern.bin
-rw-r--r-- 1 dcollin5 dcollin5 1.3K Dec 31  2009 p4xdp_drop.bin
-rwxr-xr-x 1 dcollin5 dcollin5 135K Dec 31  2009 p4udp.bin
-rwxr-xr-x 1 dcollin5 dcollin5  23K Dec 31  2009 p4pkt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  23K Dec 31  2009 p4mnl_user.bin
-rw-r--r-- 1 dcollin5 dcollin5 4.3K Dec 31  2009 p4mnl_kern.bin
-rwxr-xr-x 1 dcollin5 dcollin5 136K Dec 31  2009 p4emu.bin
-rwxr-xr-x 1 dcollin5 dcollin5  39K Dec 31  2009 p4dpdkPkt.bin
-rwxr-xr-x 1 dcollin5 dcollin5 156K Dec 31  2009 p4dpdkDbg.bin
-rwxr-xr-x 1 dcollin5 dcollin5 152K Dec 31  2009 p4dpdk.bin
-rwxr-xr-x 1 dcollin5 dcollin5 140K Dec 31  2009 p4dbg.bin
-rwxr-xr-x 1 dcollin5 dcollin5 135K Dec 31  2009 p4bench.bin
-rwxr-xr-x 1 dcollin5 dcollin5  19K Dec 31  2009 modem.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 mapInt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  19K Dec 31  2009 hdlcInt.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 dummyCon.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 daemonRun.bin
-rwxr-xr-x 1 dcollin5 dcollin5  15K Dec 31  2009 bundle.bin
```