# Introduction

MyRemote state is determined by the loaded mode file.  This is independent of the current state of the controlled devices.

MyRemote uses a json formatted file to store and configure the remote depending on the button pressed on the remote.

| field    | values                                                                                 |
| -------- | -------------------------------------------------------------------------------------- |
| type     | Required Action to take.  Valid values are `macro`, `ir`, `bluetooth`, `sleep`, `load` |
| device   | Name of the device to control as defined in lirc.                                      |
| code     | Required if type is `ir` or `bluetooth`. Code to transmit on the specified channel     |
| file     | Required if type is `load`.  Specifies the name of the file to load.                   |
| duration | Required if type is `sleep`.  Specifies the duration to sleep in seconds               |
|          |                                                                                        |

```json
    "up":{
        "type": "bluetooth",
        "device":"example_stb",
        "code":"KEY_UP"
    },

## Remote Button Presses

When a button press is received by MyRemote, one of four things can happen.

### Send IR Signal

```json
    "up":{
        "type": "bluetooth",
        "code":"KEY_UP",
        "device":"example_stb"
    },
```
The above configuration will instruct MyRemote to send the example_stb a KEY_UP code via the bluetooth channel.  Medium is determined by the device configuration.  This can be used to configure multiple devices in a give mode, for instance navigation assigned to device_1 and volume buttons assigned to device_2

### Load Another Mode File

```json
    "tv":{
       "load":"tv.json"
    },
```
The above configuration will instruct MyRemote to load the tv.json mode file.  This is used to switch the mode of the remote.

### Run Another Mode File

This functionality allows you to store common commands in a single file w/o loading it to run.

This functionally can be used to act as a macro.  For instance
``` json
    "power": {
        "run":"power_off.json"
    },
```

In this example when the power button is pressed, MyRemote will load the `power_off.json` which looks like the below.

``` json
{
    "on_load":[
        {
            "macro":[
                { "type":"ir","code":"KEY_HDMI_01", "device":"toshiba_tv", },
                { "type":"sleep","duration":"2", "device":"toshiba_tv" }
                { "type":"ir","code":"KEY_POWER_OFF", "device":"toshiba_tv" }
            ]
        },

        {
            "macro": [
                { "type": "ir", "code":"KEY_HDMI_01", "device": "yamaha_receiver"  },
                { "type":"sleep","duration":"0.5", "device":"toshiba_tv" }
                { "type": "ir", "code":"KEY_POWER_OFF","device": "yamaha_receiver" }
            ]
        }
    ],

    "on_unload": {

    }
}
```

### Simulate a different Button Press

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
            "macro": [
                { "type": "ir", "code":"KEY_POWER_ON", "device": "example_tv" },
                { "type": "sleep", "duration": "2s", "device": "example_tv" },
                { "type": "ir", "code":"KEY_HDMI_01", "device": "example_tv" }
            ]
        },
        {
            "macro": [
                { "type": "ir", "code":"KEY_POWER_ON", "device": "example_receiver"},
                { "type": "ir", "code":"KEY_HDMI_04", "device": "example_receiver" }
            ]
        }
    ],
```
The above example shows that when the mode is loaded it will instruct the `example_tv` to send the `KEY_POWER_ON` command and then switch to HDMI1, with a 2 second sleep between the two actions.  The `example_receiver` will power on and then switch to HDMI4, with a 2 second sleep between actions.  Any number of actions can be done.

``` json
    "on_unload":[
        {
            "type":"bluetooth",
            "code":"KEY_POWER_OFF",
            "device":"example_stb"
        }
    ],
```
The above example shows that when the mode is unloaded it will instruct the `example_stb` to power off via the `KEY_POWER_OFF` command.  This could be used to turn off devices when not in use.  As with the `on_load` any number of actions can be called in `on_unload`.

## Common.json

Common.json will be loaded with each mode file.  This allows for a common set of macros to be defined across multiple remotes, such as a set of device buttons used to switch modes as shown below.
``` json
{
    "power": {
        "type": "load",
        "file":"power_off.json"
    },
    "tv":{
        "type": "load",
        "file":"tv.json"
    },
    "dvd":{
        "type": "load",
       "file":"dvd.json"
    },
    "stb":{
        "type": "load",
       "file":"stb.json"
    },
}
```

The individual mode files will take precedence if the same action block is defined in both the mode file and the common.json.
