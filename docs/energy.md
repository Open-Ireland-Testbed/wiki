Energy



# Energy

# Energy Monitoring and Efficiency

The OpenIreland testbed is fully committed to providing tools to monitor and optimise energy consumption of experiments. Furthermore, to support energy efficiency and reduce the power consumption utilised within the testbed, experimental resources including USRPs and servers are turned on before experiment creation and turned off after experiment completion - using a just-in-time experiment strategy. Power management and consumption are supported by the following equipment:

* 48DCWC-16-2X100-A0: PRO1 -48VDC Remote Power Manager, (16) 10A switched outputs w/ Load-Sense, 10A GMT fuses included (other values available), dual 100A input blocks, supports two temperature/humidity probes, STI black paint
* WC- PX3-5498V = 230V, 1Ph, 32A, 24 Outlets: 18 x IEC-C13, 6 x IEC-C19, Input:IEC0309 32A, 0U, 7.4kVA, bottom-bottom-feed, iX7 controller, highresolution LCD display, sensor connection
* Raritan PX3-5190CR Outlet Metered / Outlet Switched iPDU: 230V, 16A, 8 Outlets (8x C13), Plug: C20, 1U, LCD Display, 2x USB-A, 1x USB-B, Ethernet, Serial and Sensor Port

Energy awareness and autonomy across USRP radio, server, indoor and outdoor 5G Benetel Radio equipment is support by a 9 x Raritan PDU outlets (Raritan PX3-5190CR x 3, 48DCWC-16-2X100-A0 x 5, WC- PX3-5498V x 1), 4 Enginko LoRaWAN Plugs (Energy Meter and Remote Appliance Power Switch), and an testbed PDU python API developed to support energy control, automation, and data capture.