""" Handle the commands pushed to the command queue """
import pathlib
import json
import time
import lirc


class CommandProcessor:
    """CommandProcessor"""

    def __init__(self, command_queue, activity_file):
        self.command_queue = command_queue
        self.current_activity_file = activity_file
        self.current_activity = {}
        self.client = lirc.Client()
        self.load_conf_file(self.current_activity_file)

    def start(self):
        """start"""
        while True:
            item = self.command_queue.get()
            scancode = str(item["scancode"])
            long_press = item["long_press"]
            print(f"processing scancode {scancode}, long_press {long_press}")
            if scancode in self.current_activity:
                code = self.current_activity[scancode]
                if long_press and "long_press" in code:
                    code = code["long_press"]
                self.process_code(code)
            else:
                print(f"scancode {scancode} not found")

            self.command_queue.task_done()

    def process_code(self, code: str):
        """process_code"""
        repeat = 1
        if "repeat" in code:
            repeat = code["repeat"]

        for _ in range(repeat):
            if code["type"] == "ir":
                self.send_ir(code["device"], code["code"])
                print(f"IR: {code})")
            elif code["type"] == "bluetooth":
                print(f"BLUETOOTH: {code})")
            elif code["type"] == "adb":
                print(f"ADB: {code})")
            elif code["type"] == "curl":
                print(f"CURL: {code})")
            elif code["type"] == "load":
                self.load_conf_file(code["file"])
            elif code["type"] == "sleep":
                self.sleep(code["device"], code["duration"])
            elif code["type"] == "macro":
                print(f"MACRO: {code})")
                for macro_code in code["macro"]:
                    self.process_code(macro_code)
            else:
                print(f"Unknown type({code['type']})")

    def send_ir(self, device, code):
        """send_ir"""
        print(f"IR: {device}, {code}")
        try:
            self.client.send_once(device, code)
        except lirc.exceptions.LircdCommandFailureError as error:
            print(f"Unable to send the {device} key to {code}!")
            print(error)  # Error has more info on what lircd sent back.

    def sleep(self, device, duration):
        """sleep"""
        print(f"SLEEP: {device}, {duration}")
        time.sleep(float(duration))

    def on_load(self):
        """on_load"""
        print(f"on_load: {self.current_activity_file}")
        if "on_load" in self.current_activity and self.current_activity["on_load"]:
            self.process_code(self.current_activity["on_load"])

    def on_unload(self):
        """on_unload"""
        print(f"on_unload: {self.current_activity_file}")
        if "on_unload" in self.current_activity and self.current_activity["on_unload"]:
            self.process_code(self.current_activity["on_unload"])
        self.current_activity = {}

    def load_conf_file(self, conf_file: str):
        """load_conf_file"""
        file = pathlib.Path(conf_file)
        if file.exists():
            self.on_unload()

            # read the common file
            with open("json/common.json", encoding="utf-8") as file:
                common = json.load(file)

            # read the configuration file
            with open(conf_file, encoding="utf-8") as file:
                self.current_activity = json.load(file)

            self.current_activity.update(common)
            self.current_activity_file = conf_file
            self.on_load()
        else:
            print(f"Unable to find: {conf_file}")
