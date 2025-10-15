High-Level Cloud Architecture



# High-Level Cloud Architecture

A high-level overview of OpenIreland testbed architecture is depicted in Figure 3. The physical layer, at the bottom, represents the tangible resources including servers, switches, USRPs, Optical Equipment, and so forth, at the OpenIreland testbed. The virtualisation and control layers in the middle are supported by software virtualisation technologies such as OpenStack to support cloud computing, OpenFlow and Netconf to orchestrate and manage the USRPs and physical optical network equipment. The vertical and NFV MANO layers, are supported by the Open Source Network Function Virtualization (NFV) Management and Orchestration (MANO) (OSM) software stack. The Fault tolerant and NFV Metric Collection layer offers tools to support data collection.  These elements interact with the physical and virtualisation layers to dynamically instantiate radio experiment instances at the OpenIreland testbed.

## OpenIreland Testbed Functional Layers

Logically, the OpenIreland testbed can be thought of as consisting of seven functional layers, as illustrated in Figure 3. These include:

* **Functional Elements**: The bottom layer represents the physical resources, such as servers, ROADMS, National Instruments (NI) USRPs, commercial 5G small cell equipment etc.
* **Virtualisation Layer**: To expose the functionality of physical equipment for applications, OpenIreland employs a variety of hypervisor tools and technologies. This layer provides support for open source cloud virtualisation technologies (OpenStack), SDN techniques (OpenFlow 1.3, Open vSwitch, Netconf), custom Linux images, and Software-Defined Radio (SDR) elements including GNU Radio, srsLTE(4G/5G), Open Air Interface (4G/5G).
* **Management and Orchestration Layer**: This layer supports the GENI Aggregate Manager and Open Source MANO frameworks, interacting with OpenStack cloud elements to create virtual machines and networking connections.
* **NFV Layer**: OSM supports the deployment of experimental functions across the Virtualisation and Functional Layer elements, by supporting the creation of virtual machine instances and experiment instantiation. These elements provide a fully functional orchestrator for experiments at OpenIreland.
* **Virtualised Experiments**: The next layer corresponds to the virtualised testbed resources, allocated to the experimenter for a specific period of time.
* **Experiments Orchestration and Control**: This layer sits near the top and is defined and controlled by the experimenter. It is the experiment instance environment that supports a 5G end-to-end application that can fully utilise the virtualised resources offered by the lower layers.
* **Fault tolerant and NFV Metric Collection** layer sits at the top, and offers tools such as Prometheus and Grafana to support experimental data collection.