# My_Remote

My_Remote is a universal remote hub for the Raspberry PI.  It translates keyboard presses into IR/Bluetooth (TBD)/adb commands for remote controlled devices.  It's goal is to provide a single way for controlling remote controlled devices.

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

## Usage

TBD

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[See LICENSE](https://github.com/benjaminmetzler/my_remote/blob/main/LICENSE)
