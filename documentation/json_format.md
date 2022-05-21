# Introduction

my_remote state is determined by the loaded mode file.  This is independent of the current state of the controlled devices.

my_remote uses a json formatted file to store and configure the remote depending on the button pressed on the remote.  The objects are named after the scan_code received by my_remote.  For instance the `Enter` key will have a scan_code of `28`.  Each object will contain key:value pairs defining the action and any required key:value pairs.  The valid keys are listed below.

| Key        | Data                                                                            |
| ---------- | ------------------------------------------------------------------------------- |
| type       | Required.  Action to take.  Valid values are `ir`, `bluetooth`, `adb`,          |
|            | `curl`, `app`, `sleep`,`load`, and `macro`                                      |
| device     | Name of the device to control.                                                  |
| code       | Required if type is `ir`, `bluetooth`, `adb`, `curl`, or `app`.                 |
|            | Code to transmit on the specified channel to the specified device               |
| file       | Required if type is `load`.  Specifies the name of the file to load. This       |
|            | will clear out  the current mode.                                               |
| duration   | Required if type is `sleep`.  Specifies the duration to sleep in seconds.       |
| macro      | Allows running multiple commands with a single button press.                    |
| comment    | Optional field that is not used by the code but can be used for block info.     |
| repeat     | Number of times to repeat the action.  If not set the action will be done once. |
| long_press | An actions to take if a long press ( > 1 second) is detected.                   |

Possible actions are demonstrated below.

## Send Command

### IR

```json
    "103":{
        "comment": "An up button is pressed",
        "type": "ir",
        "code":"KEY_UP",
        "device":"example_nvidia_shield",
        "long_press": {
            "type": "load",
            "file":"/home/pi/my_remote/json/example_dvd.json"
        }
    },
```

The above configuration will instruct my_remote to send the example_nvidia_shield a KEY_UP code via the IR channel.  Medium is determined by the type.

### ADB

```json
    "103":{
        "comment":"KEYCODE_DPAD_UP",
        "type": "adb",
        "code":"19",
        "device":"192.168.0.146"
    },
```

The above will send a command to the device.  `adb` also allows additional options for code: `CONNECT` and `DISCONNECT`.  Use of these options will cause my_remote to issue an `adb connect` or `adb disconnect`.  See [here](nvidia_adb.md) for more information on using adb for device control.

### Bluetooth

#### NOTE: Bluetooth is not currently implemented

Useful for devices that can accept input via a bluetooth keyboard (Nvidia Shield, Amazon Firestick)

```json
    "103":{
        "comment": "An up button is pressed",
        "type": "bluetooth",
        "code":"103",
        "repeat": 5,
        "device":"example_nvidia_shield"
    },
```

The next example does the same thing as the first, but with bluetooth.  It will repeat the command 5 times.

### curl

Useful for apps like [Kodi](https://kodi.tv/) (https://kodi.wiki/view/JSON-RPC_API)

```json
    "103":{
        "comment": "An up button is pressed",
        "type": "curl",
        "code":"-s --data-binary '{\"jsonrpc\": \"2.0\", \"method\": \"System.Suspend\", \"id\":1}' -H 'content-type: application/json;' ",
        "device":"192.168.0.88:9001/jsonrpc"
    },
```

### app

#### NOTE: app is not currently implemented

Useful for apps like can be accessed via an cli app

```json
    "103":{
        "comment": "An up button is pressed",
        "type": "app",
        "code":"TBD",
        "device":"TBD"
    },
```

### Sleep

The `sleep` command is used in macros.  This is useful for when a device might require some wait between actions.  While it can be used for it's own action, it doesn't make much sense as it will just sleep the system for the `duration`.

### Load Another Mode File

```json
    "3":{
       "load":"/home/pi/my_remote/json/example_dvd.json",
        "long_press": {
            "type": "load",
            "file":"/home/pi/my_remote/json/example_nvidia_shield.json"
        }
    },
```

The above configuration will instruct my_remote to load the example_dvd.json mode file.  This is used to switch the mode of the remote.  An alternative action will load the example_nvidia_shield.json mode file if the key is held for longer then 1 second.

long_press requires that the key up indication not be returned until the key has been released.  This can happen with some special buttons like push-to-talk buttons on HDI remote.  Also not that some remotes will send the same key multiple key down indications as long as it is pressed while other buttons will send just one key down.

### Macros

``` json
    "116":{
        "comment": "power system off macro",
        "type": "macro",
        "macro": [
            { "type": "ir", "code":"INPUT_HDMI_1" , "device": "example_tv" },
            { "type": "ir", "code":"INPUT_HDMI_4" , "device": "example_receiver" },
            { "type": "sleep", "duration": "2s"  },
            { "type": "ir", "code":"KEY_POWER_OFF" , "device": "example_tv" },
            { "type": "ir", "code":"KEY_POWER_OFF" , "device": "example_receiver" }
        ]
    }
```

Macros can be used to group multiple actions on a key press.  In the above example, the `power` button (`116`) will invoke a macro that will switch the `example_tv` and `example_receiver` to the default HDMI ports and then power off the devices.  Macros can be any length and potentially call other macros or load files (both to be tested).

## Default Actions

There are two optional actions defined for mode files: `on_load` and `on_unload`.

When a mode is loaded, my_remote will invoke the `on_load` block.  This will carry out any number of steps as shown below.

``` json
    "on_load":[
        {
            "macro": [
                { "type": "ir", "code":"KEY_POWER_ON", "device": "example_tv" },
                { "type": "ir", "code":"KEY_POWER_ON", "device": "example_receiver"},
                { "type": "sleep", "duration": "2s", "device": "example_tv" },
                { "type": "ir", "code":"KEY_HDMI_01", "device": "example_tv" },
                { "type": "ir", "code":"KEY_HDMI_04", "device": "example_receiver" }
            ]
        }
    ],
```

The above example shows that when the mode is loaded it will instruct my_remote to send the power on commands to the tv and receiver and then tell them to switch to the correct HDMI ports.  Any number of actions can be done in a macro.

``` json
    "on_unload":[
        {
            "type":"bluetooth",
            "code":"KEY_POWER_OFF",
            "device":"example_nvidia_shield"
        }
    ],
```

The above example shows that when the mode is unloaded it will instruct the `example_nvidia_shield` to power off via the `KEY_POWER_OFF` command.  This could be used to turn off devices when not in use.  As with the `on_load` any number of actions can be called in `on_unload`.

## Common.json

Common.json will be loaded with each mode file.  This allows for a common set of macros to be defined across multiple remotes, such as a set of device buttons used to switch modes.  In the below example, the volume and mute buttons are always mapped to the `example_receiver` and the power button will call a `macro` to shut the system down.  These actions will be available regardless of the active mode.

``` json
    "115":{
        "comment": "Volume Up",
        "type": "ir",
        "code": "VOLUME_UP",
        "device": "example_receiver"
    },
    "114":{
        "comment": "Volume Down",
        "type": "ir",
        "code": "VOLUME_DOWN",
        "device": "example_receiver"
    },
    "113":{
        "comment": "Mute",
        "type": "ir",
        "code": "MUTE_TOGGLE",
        "device": "example_receiver"
    },
    "116":{
        "comment": "power system off macro",
        "type": "macro",
        "macro": [
            { "type": "ir", "code":"INPUT_HDMI_1" , "device": "example_tv" },
            { "type": "ir", "code":"INPUT_HDMI_4" , "device": "example_receiver" },
            { "type": "sleep", "duration": "2s" , "device": "example_tv" },
            { "type": "ir", "code":"KEY_POWER_OFF" , "device": "example_tv" },
            { "type": "ir", "code":"KEY_POWER_OFF" , "device": "example_receiver" }
        ]
    }
}
```

The individual mode files will take precedence if the same action block is defined in both the mode file and the common.json.
