OpenIreland LoRaWAN Tutorial



# OpenIreland LoRaWAN Tutorial

# 2. References

<https://wiki.seeedstudio.com/Seeeduino_LoRAWAN/>

# 3. jFed and Fed4FIRE+ account

Email[**wireless.testbed@connectcentre.ie**](mailto:wireless.testbed@connectcentre.ie)to register for a jfedaccount (also on this URL: <https://portal.fed4fire.eu/> ). You can use your student account at your institute, oralternatively request to join the "pervasivenation" project when registering**(**[**mailto:wireless.testbed@connectcentre.ie**](mailto:wireless.testbed@connectcentre.ie)**)**

# 4. Download jFed Framework

Download jFed client software to run the RSPEC file in the next section

<https://jfed.ilabt.imec.be/downloads/>

# 5. Rspec for Seeeduino LoRAWAN Board at Iris -Support for Pervasive Nation

Load the following rspec, with connected Seeeduino LoRaWAN Board with ubuntu (<https://wiki.seeedstudio.com/Seeeduino_LoRAWAN/> )

```
<?xml version='1.0'?>
<rspec xmlns="http://www.geni.net/resources/rspec/3" type="request" generated_by="jFed RSpec Editor" generated="2022-12-09T10:51:17.720Z" xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" xmlns:jfedBonfire="http://jfed.iminds.be/rspec/ext/jfed-bonfire/1" xmlns:delay="http://www.protogeni.net/resources/rspec/ext/delay/1" xmlns:jfed-command="http://jfed.iminds.be/rspec/ext/jfed-command/1" xmlns:client="http://www.protogeni.net/resources/rspec/ext/client/1" xmlns:jfed-ssh-keys="http://jfed.iminds.be/rspec/ext/jfed-ssh-keys/1" xmlns:jfed="http://jfed.iminds.be/rspec/ext/jfed/1" xmlns:sharedvlan="http://www.protogeni.net/resources/rspec/ext/shared-vlan/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd ">
  <node client_id="vm" exclusive="true" component_manager_id="urn:publicid:IDN+iris-open-testbed.connectcentre.ie+authority+am">
    <sliver_type name="vm-seeeduino-iot-dedicated">
      <disk_image name="urn:publicid:IDN+iris-open-testbed.connectcentre.ie+image+seeeduino-board-tutorial"/>
    </sliver_type>
    <location xmlns="http://jfed.iminds.be/rspec/ext/jfed/1" x="75.0" y="25.0"/>
  </node>
</rspec>
```

# 6. Jfed

![](assets/openireland-lorawan-tutorial/52c446785741c4cddb45d3e86a7b03485ba9180197c1807152c3f42941ebe15e)

Make sure that Seeeduino board is connected to the VM at Iris, by running the following command. *dmesg | grepSeeed* - and if the board is there you should see the following information.

```
iristest@seeeduino-node:~$ dmesg | grep Seeed
[ 3.171580] usb 1-1.5: Product: Seeeduino LoRaWAN
[ 3.174509] usb 1-1.5: Manufacturer: Seeed Studio
iristest@seeeduino-node:~$
```

Note, If you cannot see the board using the above command, contact OpenIreland Testbed support team.

# 7. Download the PN TheThingsNetwork GitHub code

Clone the pervasive nation Seeeduino code or copy the contents of the file:

<https://github.com/pervasivenation/pn_seeed/blob/master/pn_seeed.ino>

```
git clone https://github.com/pervasivenation/pn_seeed.git
```

Start arduino if not already started

```
arduino
```

Open the pn\_seeed.ino file

Compile the file - using the "Verify" button

![](assets/openireland-lorawan-tutorial/ee7037081e2fc6d763a607fbd8bd9b7729fcfa16bc938379695a0638cd47c38e)

Use the "**Upload"** button to push the code to the board.

![](assets/openireland-lorawan-tutorial/c160545363e6c31364a2ac843df1f3283dfcb408ac355a13dc0f039f9162dc2b)

Note, you can see debug information from the Serial Monitor

# 8. Install the Seeduino board

Open your Arudino IDE, click on **File > Preferences**, and copy below url to *Additional Boards Manager URLs:*

```
https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json
```

![](assets/openireland-lorawan-tutorial/c269796ea8daaeb66b397d6698ca5daa43fa174373ee70f8483332134c3a84a9)

# 9. Install a board manager

Click on **Toos > Board > Board Manager**.

Now you can search the board by name "Seeduino" and install Seed SAMD Boards

![](assets/openireland-lorawan-tutorial/94a38c58813c07fc62c455a75af1a41b1ecca51b84273849d348c02a65438d51)

# 10. Set a board

After Step 3 was successful, a board named SeeeduinoLoraWan will show up at the boards list. Select it.

Click on **Tools > Board**, ***SeeeduinoLoraWan > Seeed SAMD (32-Bits ARM cortex - MO+ and Cortex-M4)Boards > Seeeduino LoRaWAN*** is available now. You may need to click this to activate it.

![](assets/openireland-lorawan-tutorial/306afe7b1eacc87f02ab22a81dfd9f6079a18644ee5b4a3b5fba999136a078c3)

When the LoRaWAN Seeeduino USB device is attached to the machine, its visible in the following screenshot. Youcan now load code to the board to support LoRaWAN seeeduino communication.

![](assets/openireland-lorawan-tutorial/9ee8fb30dd0bdcf9c4ba023b02399f6de94d06b47210a270b453111bd9b3775d)

Note, if you cannot see the board in Arduino try the following command

```
sudo apt install linux-modules-extra-$(uname -r)
#Reboot the VM and log back in.
sudo reboot
```

Note, If you cannot see the board using the above command, contact OpenIreland Testbed support team.

# 11. Add your user to the dialout group and grantpermission on the Seeduino board

```
sudo usermod -a -G dialout $USER
sudo chmod a+rw /dev/ttyACM0
```

Log out and back in again after running these commands.

# 12. Load the PN LoRaWAN Code, and execute to test it.

Download the PN LoRaWAN Code from GitHub, and use the "Upload" button to upload the code to the Seeeduinoboard.

Enable debug

![](assets/openireland-lorawan-tutorial/0da1595d2c4dfd7b2504961d40e2f7940a3d3447e8cbdc0f43f46043b45b9617)

Enable debug and view the console output.

![](assets/openireland-lorawan-tutorial/92ae6eedfcaaed553a9d976813690aa2fe4b307cfb625adef66f9bff279af3ba)

# Troubleshooting

Error

```
 fatal error: LoRaWan.h: No such file or directory
 #include <LoRaWan.h>
          ^~~~~~~~~~~
compilation terminated.
exit status 1
LoRaWan.h: No such file or directory
```

Search for file LoRaWan.h

```
sudo find / -name LoRaWan.h
```

 Create a symbolic link to the location its expected. If you don’t know what that means google it.

For example:

```
sudo ln -s /home/iristest/Arduino/libraries/Beelan_LoRaWAN/src/lorawan.h /usr/include/LoRaWan.h
```