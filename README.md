# My_Remote

My_Remote is a universal remote hub for the Raspberry PI.  It translates keyboard presses into IR/Bluetooth (TBD)/adb commands for remote controlled devices.  It's goal is to provide a single way for controlling remote controlled devices.

## Progress

```text
| Feature           | Progress       |
| ----------------- | -------------- |
| IR Support        | Working        |
| Bluetooth Support | Not Working    |
| ADB Support       | Working (slow) |

```


## Installation

My_Remote runs on a (Raspberry PI)[https://www.raspberrypi.org/] with an [IR interface](https://www.crowdsupply.com/anavi-technology/infrared-phat).

1. [Boot a Raspberry PI with the Raspberry PI OS Lite (32-bit) image.](https://www.raspberrypi.org/documentation/installation/installing-images/). You should be able to use any Raspberry PI with a
2. Insert the SD card into the Raspberry PI and boot.
3. Connect to the PI with ssh.
4. Clone the repo: `git clone git@github.com:benjaminmetzler/my_remote.git`
5. Change into the local directory: `cd my_remote`
6. Run the setup: `./setup_pi4.sh`
7. Reboot the PI
8. ssh back into the PI
9. Start the my_remote service: `sudo systemctl start my_remote`

The My_Remote service will start and listen for keystrokes from a directly connected keyboard.  Depending on the keystroke, My_Remote will take different actions.

## Design

![Architecture Diagram](documentation/MR_Diagram.png)

my_remote takes input from a keyboard or an HID remote and converts it into an appropriate format.  my_remote uses json files to it's current state. Each state defines the actions that my_remote takes when an HID button is pressed.  The format of these json files is documented [here](documentation/json_format.md).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  Help with a functional bluetooth HID is greatly appreciated.

# Links

* https://globalcache.zendesk.com/hc/en-us/articles/360034968311-iConvert-Converting-IR-code-formats
* https://www.instructables.com/Transforming-Raspberry-Pi-Into-a-Remote-Control/
* https://projects-raspberry.com/emulate-a-bluetooth-keyboard-with-the-raspberry-pi/
* https://remotesource.net/full-remote-catalog/
* https://github.com/boppreh/keyboard
* https://flirc.tv/more/flirc-usb
* https://github.com/ruundii/bthidhub
* https://github.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry

## License

[See LICENSE](https://github.com/benjaminmetzler/my_remote/blob/main/LICENSE)
