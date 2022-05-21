# Nvidia Shield ADB Usage

To connect the Nvidia shield to my_remote:

1. Enable Developer Mode on the Nvidia Shield
   1. Go to `Settings` -> `Device Preferences` -> `About`
   1. Scroll to the bottom and tap `Build Number` seven (or more) times.
   1. After seven clicks the Nvidia Shield will pop up a message about entering developer mode.
   1. Exit back to `Device Preferences` and navigate down to `Developer options`.
   1. Enable `Network debugging` and note the IP address.

1. `ssh` into the raspberry pi and type `adb connect IP_ADDRESS` where IP_ADDRESS is the IP address noted above.
1. On the Nvidia Shield it will prompt to `Allow Network debugging`.  Click the `Always allow from this computer` box and then click OK.

After you have done the above, review the `example_nvidia_shield.json` for how to use the `adb` command.  Note that in the example my_remote will attempt to connect `on_load` of the mode and disconnect `on_unload`.  This is not necessary but may be more reliable.

Also note that the adb connection is slow so the time between a press on the keyboard/remote can take longer then IR based actions.
