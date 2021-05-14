#!/usr/bin/env bash
# programs an flirc USB dongle with USB HID media keys
# from: https://kiljan.org/2019/03/30/controlling-android-tv-and-kodi-with-logitech-harmony-and-flirc/

export flirc_util=/Applications/Flirc.app/Contents/Resources/flirc_util

$flirc wait
$flirc format

echo "Press button: PowerOff" && $flirc record_api 50 102
echo "Press button: PowerOn" && $flirc record_api 1 102
echo "Press button: PowerToggle" && $flirc record_api 48 102
echo "Press button: Up" && $flirc record_api 66 102
echo "Press button: Down" && $flirc record_api 67 102
echo "Press button: Left" && $flirc record_api 68 102
echo "Press button: Right" && $flirc record_api 69 102
echo "Press button: Page up" && $flirc record_api 156 102
echo "Press button: Page down" && $flirc record_api 157 102
echo "Press button: OK" && $flirc record_api 65 102
echo "Press button: Back" && $flirc record_api 70 102
echo "Press button: Menu" && $flirc record_api 64 102
echo "Press button: Play" && $flirc record_api 176 102
# echo "Press button: Pause" && $flirc record_api 176 102
# echo "Press button: Stop" && $flirc record_api 183 102
echo "Press button: Rewind" && $flirc record_api 180 102
echo "Press button: Fast forward" && $flirc record_api 179 102
echo "Press button: 1" && $flirc record_api 0 30
echo "Press button: 2" && $flirc record_api 0 31
echo "Press button: 3" && $flirc record_api 0 32
echo "Press button: 4" && $flirc record_api 0 33
echo "Press button: 5" && $flirc record_api 0 34
echo "Press button: 6" && $flirc record_api 0 35
echo "Press button: 7" && $flirc record_api 0 36
echo "Press button: 8" && $flirc record_api 0 37
echo "Press button: 9" && $flirc record_api 0 38
echo "Press button: 0" && $flirc record_api 0 39
# echo "Press button: Clear" && $flirc record_api 0 42
# echo "Press button: Enter" && $flirc record_api 0 40
# echo "Press button: Info" && $flirc record_api 0 12
echo "Press button: Home" && $flirc record_api 8 40
