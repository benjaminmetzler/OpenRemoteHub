# Adding a new remote

OpenRemoteHub can handle any device that acts like an HID keyboard.  Most remotes sold for a computer use some set of key presses, whether they are the standard keyboard keys like 0-9 or special "hidden" keys like F11-F24.  OpenRemoteHub uses the [scancode](https://en.wikipedia.org/wiki/scancode) sent from the HID controller to map to the action.

```json
    "106":{
        "comment": "right",
        "type": "ir",
        "code": "KEY_RIGHT",
        "device": "lg_dvd"
    }
```

The above maps the scancode 106 to the KEY_RIGHT.  Depending on your HID controller it use the standard codes or it's own mapping.  The best way to determine the scancode is to use `evtest`.  This will display the keyboard events with useful extended information not returned with the `keyboard` python library.

1. Launch `evtest`
1. Select your remotes keyboard device.  This may require a couple of tries if you have multiple keyboards attached.

    ```shell
    pi@raspberrypi:~ $ evtest
    No device specified, trying to scan all of /dev/input/event*
    Not running as root, no devices may be available.
    Available devices:
    /dev/input/event0:  SG.Ltd SG Control Mic Keyboard
    /dev/input/event1:  SG.Ltd SG Control Mic Consumer Control
    /dev/input/event2:  SG.Ltd SG Control Mic System Control
    /dev/input/event3:  SG.Ltd SG Control Mic
    /dev/input/event4:  SG.Ltd SG Control Mic Keyboard
    /dev/input/event5:  SG.Ltd SG Control Mic Consumer Control
    /dev/input/event6:  SG.Ltd SG Control Mic System Control
    /dev/input/event7:  SG.Ltd SG Control Mic
    /dev/input/event8:  gpio_ir_recv
    /dev/input/event9:  Logitech Harmony 20+
    /dev/input/event10:  Virtual Keyboard
    Select the device event number [0-10]: 9
    ```

    In this case `/dev/input/event9:  Logitech Harmony 20+` was selected.

1. Press a button.  In the below it shows the up key was pressed (`code 103(KEY_UP)`).

    ```shell
    Testing ... (interrupt to exit)
    Event: time 1621660271.531453, type 4 (EV_MSC), code 4 (MSC_SCAN), value 70052
    Event: time 1621660271.531453, type 1 (EV_KEY), code 103 (KEY_UP), value 1
    Event: time 1621660271.531453, -------------- SYN_REPORT ------------
    Event: time 1621660271.687440, type 4 (EV_MSC), code 4 (MSC_SCAN), value 70052
    Event: time 1621660271.687440, type 1 (EV_KEY), code 103 (KEY_UP), value 0
    Event: time 1621660271.687440, -------------- SYN_REPORT ------------
    ```

1. Press all buttons on your remote to get each button scancode.

## Unknown scancodes

In some cases `evtest` will report an "unknown" key (code 240), as shown below:

```shell
Event: time 1621660450.904777, type 4 (EV_MSC), code 4 (MSC_SCAN), value c01ec
Event: time 1621660450.904777, type 1 (EV_KEY), code 240 (KEY_UNKNOWN), value 1
Event: time 1621660450.904777, -------------- SYN_REPORT ------------
Event: time 1621660451.064795, type 4 (EV_MSC), code 4 (MSC_SCAN), value c01ec
Event: time 1621660451.064795, type 1 (EV_KEY), code 240 (KEY_UNKNOWN), value 0
Event: time 1621660451.064795, -------------- SYN_REPORT ------------
```

In this case the scancode must be mapped at the system level for OpenRemoteHub to use them.  To do this, use the below as a template and create a file with the name `98-REMOTE_NAME.hwdb` where `REMOTE-NAME` is the name of your remote (e.g. 98-GI40.hwdb or 98-harmonycompanion.hwdb):

```shell
evdev:name:Logitech Harmony 20+:*
 KEYBOARD_KEY_c01ec=power
 KEYBOARD_KEY_c01f4=blue
 KEYBOARD_KEY_c01f5=yellow
 KEYBOARD_KEY_c01f6=green
 KEYBOARD_KEY_c01f7=red
```

The above example maps the button `c01ec` (determined by the value seen in `evtest`) to the KEY_POWER event type.  It also maps the buttons c01f4, c01f5, c01f6, and c01f7 to blue, yellow, green, and red, respectively.  The first line indicates the device that should be mapped, which you can find in the list presented by `evtest`.  The format of each line `KEYBOARD_KEY_<scancode>=<keycode>`. The value of `<scancode>` is hexadecimal but without the leading 0x (e.g. `c01ec` instead of `0xc01ec`).  The value of `<keycode>` is the lower-case keycode name string as listed in /usr/include/linux/input-event-codes.h minus the `KEY_`.  A full list of valid event types can be found in the `Keys and buttons` section [here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h).

After creating the mapping, copy the file to `/etc/udev/hwdb.d/`, and then load the mapping by running the below

```shell
sudo systemd-hwdb update
sudo udevadm trigger
```

A mapping for the Harmony Companion has already been installed to the Pi and can be used as a sample.
