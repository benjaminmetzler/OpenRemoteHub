# command_processor.py
import pathlib
import json


class CommandProcessor:
    def __init__(self, command_queue, activity_file):
        self.command_queue = command_queue
        self.current_activity_file = activity_file
        self.current_activity = {}
        self.long_press_limit = 0.75
        self.load_conf_file(self.current_activity_file)

    def start(self):
        while True:
            item = self.command_queue.get()
            self.process_code(str(item["scancode"]), item["time_elapsed"])
            self.command_queue.task_done()

    def process_code(self, code: str, time_elapsed: float):
        if code in self.current_activity:
            code = self.current_activity[code]
            if time_elapsed > self.long_press_limit and "long_press" in code:
                code = code["long_press"]
                time_elapsed = 0.0

            if "type" in code:
                if "repeat" in code:
                    repeat = code["repeat"]
                else:
                    repeat = 1
                for x in range(repeat):
                    if code["type"] == "ir":
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
                        print(f"SLEEP: {code})")
                    elif code["type"] == "macro":
                        print(f"MACRO: {code})")
                        for macro_code in code["macro"]:
                            self.process_code(macro_code, time_elapsed)
                    else:
                        print("Unknown type(%s)" % code["type"])

        else:
            print("Type not found: %s" % code)

    def on_load(self):
        print(f"on_load: {self.current_activity_file}")
        if "on_load" in self.current_activity:
            print("on_load'ing")
            # self.process_code(activity["on_load"], False)

    def on_unload(self):
        print(f"on_unload: {self.current_activity_file}")
        if "on_unload" in self.current_activity:
            print("on_unload'ing")
            # self.process_code(activity["on_unload"], False)
        self.current_activity = {}

    def load_conf_file(self, conf_file: str):
        file = pathlib.Path(conf_file)
        if file.exists():
            self.on_unload()

            # read the common file
            with open("json/common.json") as file:
                common = json.load(file)

            # read the configuration file
            with open(conf_file) as file:
                self.current_activity = json.load(file)

            self.current_activity.update(common)
            self.current_activity_file = conf_file
            self.on_load()
        else:
            print("Unable to find: %s" % conf_file)