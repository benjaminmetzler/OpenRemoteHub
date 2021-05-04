import json
import keyboard
import os
from jsonmerge import merge


class My_Remote:
    def __init__(self, conf_file):
        self.mode = {}
        self.current_mode_file = ""
        self.load_mode(conf_file)

    def process_code(self, code):
        if "type" in code:
            if code["type"] == "ir":
                self.send_ir(code["device"], code["code"])
            elif code["type"] == "bluetooth":
                self.bluetooth(code["device"], code["code"])
            elif code["type"] == "load":
                self.load_mode(code["file"])
            elif code["type"] == "sleep":
                self.sleep(code["device"], code["duration"])
            elif code["type"] == "macro":
                print()
                for macro_code in code["macro"]:
                    self.process_code(macro_code)
            else:
                print("Unknown type(%s)" % self.code["type"])
        else:
            print("Type not found: %s" % code)

    def load_mode(self, conf_file):
        self.on_unload()

        # read the common file
        # TK should we have an on_load and on_unload in the common.json?
        # TK how should they be handled?
        f = open("/home/pi/my_remote/json/common.json")
        self.common = json.load(f)
        f.close()

        # read the configuration file
        f = open(conf_file)
        self.mode = json.load(f)
        f.close()

        self.current_mode_file = conf_file
        # load up the defaults
        self.on_load()

    def send_ir(self, device, code):
        command = "irsend SEND_ONCE %s %s" % (device, code)
        print("%s | %s" % (device, command))
        # TK sanitize parameters since we are running as root
        os.system(command)

    def bluetooth(self, device, code):
        command = " %s --> bluetooth(%s)" % (device, code)
        print("%s | %s" % (device, command))
        # TK sanitize parameters since we are running as root
        # os.system("TK")

    def sleep(self, device, duration):
        command = "sleep %s" % duration
        print("%s | %s" % (device, command))
        # TK sanitize parameters since we are running as root
        # os.system(command)

    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        if name in self.mode:
            self.process_code(self.mode[name])

    def on_load(self):
        print("on_load: %s" % self.current_mode_file)
        # on load
        # currently serial, but ideally parallelized so that multiple
        # codes could be sent across different devices, with each
        # "device" getting it's own queue that can push to a single queue
        # that is then sent out the IR/RF hardware, allowing sleeps to 
        # be run in parallel with IR/RF sends.
        if "on_load" in self.mode:
            self.process_code(self.mode["on_load"])

    def on_unload(self):
        print("on_unload: %s" % self.current_mode_file)
        if "on_unload" in self.mode:
            self.process_code(self.mode["on_unload"])
        self.mode = {}

    def event_loop(self):
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote("/home/pi/my_remote/json/common.json")
    my_remote.event_loop()
