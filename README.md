# OpenRemoteHub

OpenRemoteHub is a universal remote hub running on a Raspberry PI.  It translates keyboard presses into commands for remote controlled devices.  It's goal is to provide a single way for controlling remote controlled devices via a remote control.

## Progress

| Feature           | Progress           |
| ----------------- | ------------------ |
| IR Support        | Working            |
| Bluetooth Support | Not Working        |
| ADB Support       | Not Working        |
| curl              | Not Working        |
| app calls         | Not Working        |

## Installation

OpenRemoteHub runs on a [Raspberry Pi](https://www.raspberrypi.org/) with an [IR interface](https://www.crowdsupply.com/anavi-technology/infrared-phat).

### Quick install

ssh to the raspberry pi and run the below.  This has only been tested on a newly flashed Raspberry Pi 4 with Raspberry Pi OS Lite (32-bit)(03-04-2021).

```shell
curl https://raw.githubusercontent.com/benjaminmetzler/OpenRemoteHub/main/setup_pi4.sh | bash
```

This will update the system, install the needed packages, lirc, and other miscellaneous actions.

### Long Install

If you don't feel safe just randomly running a script from the Internet:

1. [Boot a Raspberry Pi with the `Raspberry Pi OS Lite (32-bit)` image](https://www.raspberrypi.org/documentation/installation/installing-images/). Tested version is 03-04-2021.
    * Make sure to enable ssh as a directly connected keyboard could be captured by OpenRemoteHub.
1. Insert the SD card into the raspberry pi and power it up.
1. Connect to the pi with ssh.
1. Update the pi and install git.
    * `sudo apt update; sudo apt -y upgrade; sudo apt install -y git`
1. Clone the repo.
    * `git clone https://github.com/benjaminmetzler/OpenRemoteHub.git`
1. Change into the local directory
    * `cd OpenRemoteHub`
1. Run the setup.  The pi will reboot after the script has finished.
    * `sh setup_pi4.sh`
1. ssh back into the pi
1. cd into the OpenRemoteHub directory and run main.sh
    * `cd OpenRemoteHub; bash main.sh`

OpenRemoteHub will start and listen for keystrokes from a directly connected keyboard.  Depending on the keystroke, OpenRemoteHub will take different actions.  When first booted, it will load the `json/common.json` file.

## Design

![Architecture Diagram](documentation/MR_Diagram.png)

OpenRemoteHub takes input from a keyboard or an HID remote and converts it into an appropriate format.  OpenRemoteHub uses json files to it's current state. Each state defines the actions that OpenRemoteHub takes when an HID button is pressed.  The format of these json files is documented [here](documentation/json_format.md).

## Contributing

Pull requests are welcome. Help with enabling the Raspberry Pi as a functional bluetooth HID to an android device (think Nvidia Shield or Apple TV) is greatly appreciated.  For major changes, please open an issue first to discuss what you would like to change.

The code is written with VSCode in mind. It has a configuration set up in the .vscode directory that allows for debugging. To do development, take the following steps:

1. Run the prep command: `./prep`. This will:
    1. Create a virtual environment
    1. Install the requirement.txt into the venv
    1. Install pre-commit pre-commit hook
1. Activate the virtual env for your development: `source venv/bin/activate`

Please ensure that any PRs pass pre-commit.

## Docker Container

I'd want OpenRemoteHub into a container to avoid having to build everything into the OS. The main issue with this is that the USB remote controls tend to show up as an HID device and get picked up by the kernel, as shown below:

``` log
ben@scratch:~ $ sudo dmesg -c
[  898.433073] usb 1-1.1.3: USB disconnect, device number 4
[  900.132667] usb 1-1.1.3: new full-speed USB device number 8 using dwc_otg
[  900.277177] usb 1-1.1.3: New USB device found, idVendor=0c40, idProduct=7a1c, bcdDevice= 2.00
[  900.277216] usb 1-1.1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[  900.277236] usb 1-1.1.3: Product: SG Control Mic
[  900.277253] usb 1-1.1.3: Manufacturer: SG.Ltd
[  900.311884] input: SG.Ltd SG Control Mic Keyboard as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.3/1-1.1.3:1.2/0003:0C40:7A1C.0009/input/input11
[  900.373615] hid-generic 0003:0C40:7A1C.0009: input,hidraw0: USB HID v1.01 Keyboard [SG.Ltd SG Control Mic] on usb-3f980000.usb-1.1.3/input2
[  900.377430] input: SG.Ltd SG Control Mic as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.3/1-1.1.3:1.3/0003:0C40:7A1C.000A/input/input12
[  900.377897] hid-generic 0003:0C40:7A1C.000A: input,hidraw1: USB HID v1.01 Mouse [SG.Ltd SG Control Mic] on usb-3f980000.usb-1.1.3/input3
```

The hid-generic is built into the kernel, so there doesn't appear to be a way to disable it. As a result, the RF remotes that emulate keyboards will always get attached to the kernel, preventing it from being controlled by a docker container...At least as far as I can tell.

## Links

* https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md
* https://globalcache.zendesk.com/hc/en-us/articles/360034968311-iConvert-Converting-IR-code-formats
* https://www.instructables.com/Transforming-Raspberry-Pi-Into-a-Remote-Control/
* https://projects-raspberry.com/emulate-a-bluetooth-keyboard-with-the-raspberry-pi/
* https://remotesource.net/full-remote-catalog/
* https://github.com/boppreh/keyboard
* https://flirc.tv/more/flirc-usb
* https://github.com/ruundii/bthidhub
* https://github.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry
* https://www.lirc.org
* https://www.raspberrypi.org/
* https://www.crowdsupply.com/anavi-technology/infrared-phat
* https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md
* https://www.aliexpress.com/item/1005001714763038.html
* https://github.com/mtlynch/key-mime-pi

## License

[See LICENSE](https://github.com/benjaminmetzler/OpenRemoteHub/blob/main/LICENSE)
