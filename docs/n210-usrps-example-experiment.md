N210 USRPs - Example Experiment



# N210 USRPs - Example Experiment

This is an example experiment for instantiating N210 USRPs supported by the OpenIreland API

```
<?xml version='1.0'?>
<rspec xmlns="http://www.geni.net/resources/rspec/3" type="request" generated_by="jFed RSpec Editor" generated="2022-12-20T18:05:48.291Z" xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" xmlns:jfedBonfire="http://jfed.iminds.be/rspec/ext/jfed-bonfire/1" xmlns:delay="http://www.protogeni.net/resources/rspec/ext/delay/1" xmlns:jfed-command="http://jfed.iminds.be/rspec/ext/jfed-command/1" xmlns:client="http://www.protogeni.net/resources/rspec/ext/client/1" xmlns:jfed-ssh-keys="http://jfed.iminds.be/rspec/ext/jfed-ssh-keys/1" xmlns:jfed="http://jfed.iminds.be/rspec/ext/jfed/1" xmlns:sharedvlan="http://www.protogeni.net/resources/rspec/ext/shared-vlan/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd ">
  <node client_id="n210" exclusive="true" component_manager_id="urn:publicid:IDN+iris-open-testbed.connectcentre.ie+authority+am" component_id="urn:publicid:IDN+iris-open-testbed.connectcentre.ie+node+n210-10.55.24.0">
    <sliver_type name="vm-m1.n210.medium">
      <disk_image name="urn:publicid:IDN+iris-open-testbed.connectcentre.ie+image+jammy"/>
    </sliver_type>
    <location xmlns="http://jfed.iminds.be/rspec/ext/jfed/1" x="75.0" y="25.0"/>
    <interface client_id="n210:ens3">
      <ip address="provider3" type="ipv4"/>
    </interface>
  </node>
</rspec>
```

![](assets/n210-usrps-example-experiment/d90385d933aed626ebbb015feafa770616766c2aeba7541c8b7a60e61c542e17)

Run the Experiment

The latest version of Ubuntu is used, downloaded nightly

To view the USRPs run the following commands

```
sudo apt-get update
sudo apt install net-tools -y
sudo apt-get install libuhd-dev uhd-host -y
```

Benchmark test the USRP.

```
cd /usr/lib/uhd/examples
./benchmark_rate --rx_rate 20e6 --tx_rate 20e6 --duration 30
##You should see output as follows:
Benchmark rate summary:
Num received samples: 302084340
Num dropped samples: 0
Num overruns detected: 0
Num transmitted samples: 308295260
Num sequence errors (Tx): 0
Num sequence errors (Rx): 0
Num underruns detected: 0
Num late commands: 0
Num timeouts (Tx): 0
Num timeouts (Rx): 0
```

For USRP - VM performance trips check out the following link. This might be necessary if the benchmark tests fail.

<https://kb.ettus.com/USRP_Host_Performance_Tuning_Tips_and_Tricks>

# Reference

# N210 USRPs attached to Switch + port 22 Dec 2022

| **USRP Name** | **Cable Colour** | **Cable Number** | **Dell Switch Port** | **OI - IP Address** |
| --- | --- | --- | --- | --- |
| N210\_Sandbox\_4  N210\_D1\_2 | Orange | 16 | 48 | 10.55.41.2 |
| N210\_Sandbox\_4  N210\_D1\_1 | White | 13 | 33 | 10.55.40.2 |
| N210\_C1\_1 | Orange | 12 | 47 | 10.55.25.2 |
| N210\_C1\_2 | White | 14 |  | 10.55.26.2 |
| N210\_C23\_1 | orange | 11 | 46 | 10.55.27.2 |
| N210\_C23\_2 | white | 22 | 34 | 10.55.28.2 |
| N210\_sandbox\_5  (N210\_c34\_1) | white | 26 |  | 10.55.30.2 |
| N210\_sandbox\_5  (N210\_c34\_2) | orange | 9 | 45 | 10.55.29.2 |
| N210\_b4\_3 | orange | 5 | 44 | 10.55.42.2 |
| N210\_b4\_4 | white | 27 |  | 10.55.50.2 |
| N210\_b23\_4 | white | 23 | 36 | 10.55.51.2 |
| N210\_b23\_3 | orange | 9 or 6 | 42 | 10.55.52.2 |
| N210\_b23\_2 | orange | 7 | 43 | 10.55.53.2 |
| N210\_b23\_1 | white | 19 |  | 10.55.54.2 |
| N210\_b12\_1 | orange | 8 | 41 | 10.55.55.2 |
| N210\_a34\_2 | white | 28 | 35 | 10.55.56.2 |
| N210\_a34\_1 | orange | 4 | 40 | 10.55.57.2 |
| N210\_a23\_4 | orange | 3 | 38 | 10.55.58.2 |
| N210\_a23\_3 | white | 24 | 37 | 10.55.59.2 |
| N210\_sandbox\_3  N210\_a23\_2 | Orange | 2 | 39 | 10.55.23.2 |
| N210\_sandbox\_3  N210\_a23\_1 | white | 20 |  | 10.55.24.2 |