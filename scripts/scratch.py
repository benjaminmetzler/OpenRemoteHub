import json
import keyboard
import os

class My_Remote:
    def __init__(self, conf_file):
        self.mode = {}

    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        print("%s(%s)" % (scan_code, name))

    def event_loop(self):
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote("/home/pi/my_remote/json/my_stb.json")
    my_remote.event_loop()
