# Introduction

OpenRemoteHub state is determined by the loaded activity file. This is independent of the current state of the controlled devices.

OpenRemoteHub uses a json formatted file to store and configure the remote depending on the button pressed on the remote. The objects are named after the scancode received by OpenRemoteHub. For instance the `Enter` key will have a scancode of `28`. Each object will contain key:value pairs defining the action and any required key:value pairs.

## Valid Keys

**action**: Action to take. Valid values are `ir`, `bluetooth`, `adb`, `curl`, `app`, `sleep`,`load`, and `macro`

**code**: Code to transmit on the specified channel to the specified device. Required if action is `ir`, `bluetooth`, `adb`, `curl`, or `app`.

**comment**: Optional field that is not used by the code but can be used for block info.

**device**: Name of the device to control

**duration**: Required if action is `sleep`. Specifies the duration to sleep in seconds. Can be a float or int (0.25 or 1)

**file**: Specifies the name of the file to load. This will clear out the current activity. Required if action is `load`.

**long_press**: An actions to take if a long press ( > 1 second) is detected.

**macro**: Allows running multiple commands with a single button press.

**repeat**: Number of times to repeat the action. If not set the action will be done once.

## Examples

### IR

```json
    "103":{
        "comment": "An up button is pressed",
        "action": "ir",
        "code":"KEY_UP",
        "device":"example_stb",
        "long_press": {
            "action": "load",
            "file":"json/example_dvd.json"
        }
    },
```

The above configuration will instruct OpenRemoteHub to send the example_stb a KEY_UP code via the IR channel. Medium is determined by the action.

### ADB

#### NOTE: ADB is not currently implemented


```json
    "103":{
        "comment":"KEYCODE_DPAD_UP",
        "action": "adb",
        "code":"19",
        "device":"192.168.0.146"
    },
```

The above will send a command to the device. `adb` also allows additional options for code: `CONNECT` and `DISCONNECT`. Use of these options will cause OpenRemoteHub to issue an `adb connect` or `adb disconnect`. See [here](nvidia_adb.md) for more information on using adb for device control.

### Bluetooth

#### NOTE: Bluetooth is not currently implemented

Useful for devices that can accept input via a bluetooth keyboard (Nvidia Shield, Amazon Firestick)

```json
    "103":{
        "comment": "An up button is pressed",
        "action": "bluetooth",
        "code":"103",
        "repeat": 5,
        "device":"example_stb"
    },
```

The next example does the same thing as the first, but with bluetooth. It will repeat the command 5 times.

### curl

#### NOTE: curl is not currently implemented

Useful for apps like [Kodi](https://kodi.tv/) (https://kodi.wiki/view/JSON-RPC_API)

```json
    "103":{
        "comment": "An up button is pressed",
        "action": "curl",
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
        "action": "app",
        "code":"TBD",
        "device":"TBD"
    },
```

### Sleep

The `sleep` command is used in macros. This is useful for when a device might require some wait between actions. While it can be used for it's own action, it doesn't make much sense as it will just sleep the system for the `duration`.

### Load Another Activity File

```json
    "3":{
       "load":"json/example_dvd.json",
        "long_press": {
            "action": "load",
            "file":"json/example_stb.json"
        }
    },
```

The above configuration will instruct OpenRemoteHub to load the example_dvd.json activity file. This is used to switch the activity of the remote. An alternative action will load the example_stb.json activity file if the key is held for longer then 1 second.

long_press requires that the key up indication not be returned until the key has been released. This can happen with some special buttons like push-to-talk buttons on HDI remote. Also not that some remotes will send the same key multiple key down indications as long as it is pressed while other buttons will send just one key down.

### Macros

``` json
    "116":{
        "comment": "power system off macro",
        "action": "macro",
        "macro": [
            { "action": "ir", "code":"INPUT_HDMI_1" , "device": "example_tv" },
            { "action": "ir", "code":"INPUT_HDMI_4" , "device": "example_receiver" },
            { "action": "sleep", "duration": "2"  },
            { "action": "ir", "code":"KEY_POWER_OFF" , "device": "example_tv" },
            { "action": "ir", "code":"KEY_POWER_OFF" , "device": "example_receiver" }
        ]
    }
```

Macros can be used to group multiple actions on a key press. In the above example, the `power` button (`116`) will invoke a macro that will switch the `example_tv` and `example_receiver` to the default HDMI ports and then power off the devices. Macros can be any length and potentially call other macros or load files (both to be tested).

## Default Actions

There are two optional actions defined for activity files: `on_load` and `on_unload`.

When a activity is loaded, OpenRemoteHub will invoke the `on_load` block. This will carry out any number of steps as shown below.

``` json
    "on_load":[
        {
            "macro": [
                { "action": "ir", "code":"KEY_POWER_ON", "device": "example_tv" },
                { "action": "ir", "code":"KEY_POWER_ON", "device": "example_receiver"},
                { "action": "sleep", "duration": "2", "device": "example_tv" },
                { "action": "ir", "code":"KEY_HDMI_01", "device": "example_tv" },
                { "action": "ir", "code":"KEY_HDMI_04", "device": "example_receiver" }
            ]
        }
    ],
```

The above example shows that when the activity is loaded it will instruct OpenRemoteHub to send the power on commands to the tv and receiver and then tell them to switch to the correct HDMI ports. Any number of actions can be done in a macro.

``` json
    "on_unload":[
        {
            "action":"bluetooth",
            "code":"KEY_POWER_OFF",
            "device":"example_stb"
        }
    ],
```

The above example shows that when the activity is unloaded it will instruct the `example_stb` to power off via the `KEY_POWER_OFF` command. This could be used to turn off devices when not in use. As with the `on_load` any number of actions can be called in `on_unload`.

## Common.json

Common.json will be loaded with each activity file. This allows for a common set of macros to be defined across multiple remotes, such as a set of device buttons used to switch activities as shown below. In the below example, the volume and mute buttons are always mapped to the `example_receiver` and the power button will call a `macro` to shut the system down. These actions will be available regardless of the active activity.

``` json
    "115":{
        "comment": "Volume Up",
        "action": "ir",
        "code": "VOLUME_UP",
        "device": "example_receiver"
    },
    "114":{
        "comment": "Volume Down",
        "action": "ir",
        "code": "VOLUME_DOWN",
        "device": "example_receiver"
    },
    "113":{
        "comment": "Mute",
        "action": "ir",
        "code": "MUTE_TOGGLE",
        "device": "example_receiver"
    },
    "116":{
        "comment": "power system off macro",
        "action": "macro",
        "macro": [
            { "action": "ir", "code":"INPUT_HDMI_1" , "device": "example_tv" },
            { "action": "ir", "code":"INPUT_HDMI_4" , "device": "example_receiver" },
            { "action": "sleep", "duration": "2" , "device": "example_tv" },
            { "action": "ir", "code":"KEY_POWER_OFF" , "device": "example_tv" },
            { "action": "ir", "code":"KEY_POWER_OFF" , "device": "example_receiver" }
        ]
    }
}
```

The individual activity files will take precedence if the same action block is defined in both the activity file and the common.json.
