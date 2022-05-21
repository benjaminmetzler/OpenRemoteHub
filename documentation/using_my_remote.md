# Using my_remote

My Remote uses the hub model.  A low power device (like a Raspberry Pi) will handle the state of the hub, with the actual remote being just a "dumb" device that send signals to the hub.  The hub will decide what happens when the play button is pressed depending on the state of the hub.

The hub will have modes.  My Remote will do different things based on the current mode it is in.  If it's in DVD mode, it will send the PLAY button press using the DVD PLAY IR code.  If it's in nvidia_shield mode, then an bluetooth UP press will be sent to the nvidia_shield.  my_remote tracks its mode only.  The hub doesn't know the state of the devices.

Devices that can be controlled by one of the supported my_remote interfaces can be added to my_remote.

## Infrared

Infrared (IR) support is fully functional via the lirc interface.

1. Find an lirc IR conf file for your device.  Ideally the device should have discrete access to power and input ports (for display or receivers).  Devices of the same type from the same manufacturer generally (but not always) keeps the same IR codes for each version of the device type, so BRAND TV model X will use the same IR codes for BRAND TV model Y or Z.  A good source for discrete codes are the [jp1](http://www.hifi-remote.com/forums/viewforum.php?f=25&sid=db546d7dec051a09a60b89f711ca1db8) and [remotecentral.com](http://www.remotecentral.com/cgi-bin/mboard/rc-discrete/list.cgi) forums.
1. Put the conf file in the /etc/lirc/lirc.d.conf/ directory.
1. Create a new mode json file to control this device.  This will include macros.  See the examples found in the `json` directory.  Use the `documenation/json_format.md` to understand how to create new device entries.
1. Modify common.json to load your custom mode json.  See the common.json to understand how to load new mode files.

## Bluetooth

Bluetooth support is not working at this time.

## ADB

Preliminary support for ADB commands is available.  See `documentation/nvidia_adb.conf` for how to set it up with an nvidia shield.  Other android devices should also work.
