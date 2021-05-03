# Introduction

MyRemote state is determined by the loaded mode file.  This is independent of the current state of the controlled devices.

MyRemote uses a json formated file to store and configure the remote depending on the button pressed on the remote.

## Remote Button Presses

When a button press is received by MyRemote, one of three things can happen.

### Send IR Signal

```json
    "up":{
        "device":"example_stb",
        "code":"KEY_UP"
    },
```
The above configuration will instruct MyRemote to send the example_stb a KEY_UP code.  Medium is determined by the device configuration.  This can be used to configure multiple devices in a give mode, for instance navigation assigned to device_1 and volume buttons assigned to device_2

### Load Another Mode File

```json
    "tv":{
       "switch_mode":"tv.json"
    },
```
The above configuration will instruct MyRemote to load the tv.json mode file.  This is used to switch the mode of the remote.


This functioanlty can also be used to act as a macro.  For instance
``` json
    "power": {
        "load":"power_off.json"
    },
```

In this example when the power button is pressed, MyRemote will load the `power_off.json` which looks like the below.

``` json
{
    "on_load":[
        {
            "device":"example_tv",
            "code":"KEY_HDMI_01",
            "code2":"KEY_POWER_OFF"
        },
        {
            "device":"example_tv",
            "code":"KEY_HDMI_04",
            "code2":"KEY_POWER_OFF"
        },
        {
            "device":"example_stb",
            "code":"KEY_POWER_OFF"
        },
        {
            "device":"example_dvd",
            "code":"KEY_POWER_OFF"
        },
    ],
    "on_unload": {

    }
}
```

### Simulate a Button Press

```json
    "setup": {
        "device":"example_stb",
        "button":"menu"
    },
```
The above configuration will instruct MyRemote to call the menu button block when the setup button is called.  This allows multiple buttons to be linked to one action.

## Default Actions

There are two optional actions defined for mode files: `on_load` and `on_unload`.

When a mode is loaded, MyRemote will invoke the `on_load` block.  This will carry out any number of steps as shown below.
``` json
    "on_load":[
        {
            "device":"example_tv",
            "code":"KEY_POWER_ON",
            "sleep": "2s",
            "code2":"KEY_HDMI_01"
        },
        {
            "device":"example_receiver",
            "code":"KEY_POWER_ON",
            "sleep": "2s",
            "code2":"KEY_HDMI_04"
        }
    ],
```
The above example shows that when the mode is loaded it will instruct the `example_tv` to send the `KEY_POWER_ON` command and then switch to HDMI1, with a 2 second sleep between the two actions.  The `example_receiver` will power on and then  switch to HDMI4, with a 2 second sleep between actions.  Any number of actions can be done.

``` json
    "on_unload":[
        {
            "device":"example_stb",
            "code":"KEY_POWER_OFF",
        }
    ],
```
The above example shows that when the mode is unloaded it will instruct the `example_stb` to power off via the `KEY_POWER_OFF` command.  This could be used to turn off devices when not in use.  As with the `on_load` any number of actions can be called in `on_unload`.

## Common.json

Common.json will be loaded with each mode file.  This allows for a common set of macros to be defined across multiple remotes, such as a set of device buttons used to switch modes as shown below.
``` json
{
    "power": {
        "switch_mode":"power_off.json"
    },
    "tv":{
        "switch_mode":"power_off.json"
    },
    "dvd":{
       "switch_mode":"dvd.json"
    },
    "stb":{
       "switch_mode":"stb.json"
    },
}
```

The individual mode files will take precedence if the same action block is defined in both the mode file and the common.json.