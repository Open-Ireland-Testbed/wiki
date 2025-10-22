Freertr Tutorial 2



# Freertr Tutorial 2

In the previous tutorial we worked on a simple example where we implemented two routers within a node. In this tutorial, we’ll work on-

* How to implement 4 routers in a node.
* Adding 2 interfaces (eth1 and eth2) for each router
* Explaining interconnection with all these routers using text and software files.

# Let’s get started!

In order to get started, we need to follow the same steps which are described in the previous tutorial. Such as connecting jFed and installing freeRtR while going forward to configure files. Let’s skip the initial setup part as we already have done it. In case you haven’t completed the first tutorial, feel free to go back following this link, and start from scratch! ![(big grin)](assets/freertr-tutorial-2/a1b6031110b91ed56ae49dadadf83c3fcac121c5e30345a048d1d61136d5dce6)

# Wait, understand the Diagram first before configuration!

If you understand the diagram and get an idea of what we are going to do … then both the configuration and troubleshooting would be easy for you. Essentially 4 routers are connected with each other in a way where it looks like we’ve created a loop.

![](assets/freertr-tutorial-2/5c79c7a40be61d8edc8411ee5e3ed82088b3d787b7b39e153906701a2110bbcf)

## Router 1:

As mentioned earlier, router 1 has 2 interfaces (eth1 & eth2).

* `r1@eth1` has socket `127.0.0.1 1001` and is connected to `127.0.0.1 2001`
* `r1@eth2` has socket `127.0.0.1 1002` and is connected to `127.0.0.1 3002`

## Router 2:

* `r2@eth1` has socket `127.0.0.1 2001` and is connected to `127.0.0.1 1001`
* `r2@eth2` has socket `127.0.0.1 2002` and is connected to `127.0.0.1 4002`

## Router 3:

* `r3@eth1` has socket `127.0.0.1 3001` and is connected to `127.0.0.1 4001`
* `r3@eth2` has socket `127.0.0.1 3002` and is connected to `127.0.0.1 1002`

# Configuration

Similar to the previous tutorial, we created software and hardware files for each router.

R1:

`vi r1-hw.txt`

```
int eth1 eth 0000.1111.0001 127.0.0.1 1001 127.0.0.1 2001
int eth2 eth 0000.1111.0002 127.0.0.1 1002 127.0.0.1 3002
```

Remove any blank gaps in between two lines.

`vi r1-sw.txt`

```
hostname r1
!
vrf def v1
 rd 1:1 
 exit
server telnet tel
 security protocol tel
 vrf v1
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.1 255.255.255.255
 ipv6 addr 4321::1 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1
 desc r1@eth1 -> r2@eth1
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.1 255.255.255.252
 ipv6 addr 1234:1::1 ffff:ffff::
 exit
int eth2
 desc r1@eth2 -> r3@eth2
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.5 255.255.255.252
 ipv6 addr 1234:2::1 ffff:ffff::
 exit
!
```

R2:

`vi r2-hw.txt`

```
int eth1 eth 0000.2222.0001 127.0.0.1 2001 127.0.0.1 1001
int eth2 eth 0000.2222.0002 127.0.0.1 2002 127.0.0.1 4002
```

`vi r2-sw.txt`

```
hostname r2
!
vrf def v1
 rd 1:1
 exit
server telnet tel
 security protocol tel
 vrf v1
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.2 255.255.255.255
 ipv6 addr 4321::2 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1
 desc r2@eth1 -> r1@eth1
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.2 255.255.255.252
 ipv6 addr 1234:1::2 ffff:ffff::
 exit
int eth2
 desc r2@eth2 -> r4@eth2
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.9 255.255.255.252
 ipv6 addr 1234:3::1 ffff:ffff::
 exit
!
```

R3:

`vi r3-hw.txt`

```
int eth1 eth 0000.4444.0001 127.0.0.1 4001 127.0.0.1 3001
int eth2 eth 0000.4444.0002 127.0.0.1 4002 127.0.0.1 2002
```

`vi r3-sw.txt`

```
hostname r3
!
vrf def v1
 rd 1:1
 exit
server telnet tel
 security protocol tel
 vrf v1
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.3 255.255.255.255
 ipv6 addr 4321::3 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1
 desc r3@eth1 -> r4@eth1
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.13 255.255.255.252
 ipv6 addr 1234:4::1 ffff:ffff::
 exit
int eth2
 desc r3@eth2 -> r1@eth2
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.6 255.255.255.252
 ipv6 addr 1234:2::2 ffff:ffff::
 exit
!
```

R4:

`vi r4-hw.txt`

```
int eth1 eth 0000.4444.0001 127.0.0.1 4001 127.0.0.1 3001
int eth2 eth 0000.4444.0002 127.0.0.1 4002 127.0.0.1 2002
```

`r4-sw.txt`

```
hostname r4
!
vrf def v1
 rd 1:1
 exit
server telnet tel
 security protocol tel
 vrf v1
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.4 255.255.255.255
 ipv6 addr 4321::4 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1
 desc r4@eth1 -> r3@eth1
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.14 255.255.255.252
 ipv6 addr 1234:4::2 ffff:ffff::
 exit
int eth2
 desc r4@eth2 -> r2@eth2
 lldp ena
 vrf for v1
 ipv4 addr 1.1.1.10 255.255.255.252
 ipv6 addr 1234:3::2 ffff:ffff::
 exit
!
```

# Launch all routers

Now that we have configured everything. Open 4 different terminals for each router.

Use tmux to operate 4 windows in a single frame.

R1

```
sudo java -jar rtr.jar routersc r1-hw.txt r1-sw.txt
```

R2

```
sudo java -jar rtr.jar routersc r1-hw.txt r1-sw.txt
```

R3

```
sudo java -jar rtr.jar routersc r3-hw.txt r3-sw.txt
```

R4

```
sudo java -jar rtr.jar routersc r4-hw.txt r4-sw.txt
```

## Let’s check the connectivity first by following one command-

```
sh lldp nei
```

![](assets/freertr-tutorial-2/88344a5d388284569605c964a5a5115549e91dfc386f8c22a8af47ccbe0a25c4)![](assets/freertr-tutorial-2/7348c5b0fc7ab1d47d4f3bc91f6c4502da1ee6411a956f774e16559f7f2a6532)![](assets/freertr-tutorial-2/16d11ed682fe680c988f69693f8421b7decbf4ab04022eba1f0301538b9ce8fc)![](assets/freertr-tutorial-2/c8a4aa8505efb9cd20683fffa0faa39579980b880fa546dcd2fd19b68ac118e1)

Now, Ping each other

R1

```
ping 1.1.1.2 vrf v1                                                        
pinging 1.1.1.2, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 216, min/avg/max/dev rtt=0/6.6/16/39.0, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r1#ping 1234:1::2 vrf v1                                                      
pinging 1234:1::2, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 23, min/avg/max/dev rtt=1/2.4/5/2.2, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                       
r1#ping 1.1.1.6 vrf v1                                                        
pinging 1.1.1.6, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 8, min/avg/max/dev rtt=0/1.0/2/0.4, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r1#ping 1234:2::2 vrf v1                                                      
pinging 1234:2::2, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 92, min/avg/max/dev rtt=2/8.8/17/42.9, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
r1#
```

R2

```
r2#ping 1234:1::1 vrf v1                                                      
pinging 1234:1::1, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 159, min/avg/max/dev rtt=1/4.6/15/29.4, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                      
r2#ping 1.1.1.1 vrf v1                                                        
pinging 1.1.1.1, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 12, min/avg/max/dev rtt=0/1.8/7/6.9, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                      
r2#ping 1.1.1.10 vrf v1                                                       
pinging 1.1.1.10, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 13, min/avg/max/dev rtt=1/2.0/5/2.4, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r2#ping 1234:3::2 vrf v1                                                      
pinging 1234:3::2, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 61, min/avg/max/dev rtt=1/8.6/17/51.8, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
```

R3

```
r3#ping 1.1.1.14 vrf v1                                                       
pinging 1.1.1.14, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 106, min/avg/max/dev rtt=0/0.2/1/0.1, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                    
r3#ping 1234:4::2 vrf v1                                                      
pinging 1234:4::2, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 8, min/avg/max/dev rtt=1/1.0/1/0.0, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                      
r3#ping 1.1.1.5 vrf v1                                                        
pinging 1.1.1.5, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 8, min/avg/max/dev rtt=0/1.2/3/0.9, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r3#ping 1234:2::1 vrf v1                                                      
pinging 1234:2::1, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 17, min/avg/max/dev rtt=0/2.8/8/8.5, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
r3#
```

R4

```
r4#ping 1.1.1.13 vrf v1                                                       
pinging 1.1.1.13, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 226, min/avg/max/dev rtt=1/7.4/13/15.4, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r4#ping 1234:4::1 vrf v1                                                      
pinging 1234:4::1, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 77, min/avg/max/dev rtt=2/7.6/13/20.2, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                      
r4#ping 1.1.1.9 vrf v1                                                        
pinging 1.1.1.9, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 12, min/avg/max/dev rtt=1/2.2/6/3.7, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
                                                     
r4#ping 1234:3::1 vrf v1                                                      
pinging 1234:3::1, src=null, vrf=v1, cnt=5, len=64, df=false, tim=1000, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, alrt=-1, sweep=false, multi=false
!!!!!
result=100.0%, recv/sent/lost/err=5/5/0/0, took 45, min/avg/max/dev rtt=0/8.4/25/81.8, ttl 255/255/255/0.0, tos 0/0.0/0/0.0
r4#
```

Congratulations! you have accomplished this tutorial. Let’s move forward to the next one, excited?