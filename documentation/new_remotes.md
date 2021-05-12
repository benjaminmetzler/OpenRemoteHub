# Adding a new remote

my_remote can handle any device that acts like an HID keyboard.  Most remotes sold for a computer use some set of key presses, whether they are the standard keyboard keys like 0-9 or special "hidden" keys like F11-F24.  my_remote uses the [scancode](https://en.wikipedia.org/wiki/Scancode) sent from the HID controller to map to the action.

```json
    "106":{
        "comment": "right",
        "type": "ir",
        "code": "KEY_RIGHT",
        "device": "lg_dvd"
    }
```

The above maps the scancode 104 to the KEY_RIGHT.  Depending on your HID controller it use the standard codes or it's own mapping.  They only way to figure it out is to print the scancode sent by the HID controller.  The below script (found [here](../scripts/keyboard_loop.py)) will print out the scan codes received by from an HID controller.  Run the script and it will print out the scan codes of any button press it receives.

```python
import keyboard


class My_Remote:
    def __init__(self):
        print("waiting for keystroke")

    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        print("%s(%s)" % (scan_code, name))

    def start(self):
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote()
    my_remote.start()
```
