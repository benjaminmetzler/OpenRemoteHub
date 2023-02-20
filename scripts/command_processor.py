""" Handle the commands pushed to the command queue """
import pathlib
import json
import lirc


class CommandProcessor:
    def __init__(self, command_queue, activity_file):
        self.command_queue = command_queue
        self.current_activity_file = activity_file
        self.current_activity = {}
        self.long_press_limit = 0.75
        self.client = lirc.Client()
        self.load_conf_file(self.current_activity_file)

    def start(self):
        while True:
            item = self.command_queue.get()
            scancode = str(item["scancode"])
            time_elapsed = item["time_elapsed"]
            if scancode in self.current_activity:
                code = self.current_activity[scancode]
                if time_elapsed > self.long_press_limit and "long_press" in code:
                    code = code["long_press"]
                self.process_code(code)
            else:
                print("scancode not found: {scancode}")

            self.command_queue.task_done()

    def process_code(self, code: str):
        repeat = 1
        if "repeat" in code:
            repeat = code["repeat"]

        for x in range(repeat):
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
                print(f"SLEEP: {code})")
            elif code["type"] == "macro":
                print(f"MACRO: {code})")
                for macro_code in code["macro"]:
                    self.process_code(macro_code)
            else:
                print("Unknown type(%s)" % code["type"])

    def send_ir(self, device, code):
        command = 'irsend SEND_ONCE "%s" "%s"' % (device, code)
        print("%s | %s" % (device, command))
        try:
            self.client.send_once(device, code)
        except lirc.exceptions.LircdCommandFailureError as error:
            print("Unable to send the %s key to %s!" % (device, code))
            print(error)  # Error has more info on what lircd sent back.

    def on_load(self):
        print(f"on_load: {self.current_activity_file}")
        if "on_load" in self.current_activity and self.current_activity["on_load"]:
            self.process_code(self.current_activity["on_load"])

    def on_unload(self):
        print(f"on_unload: {self.current_activity_file}")
        if "on_unload" in self.current_activity and self.current_activity["on_unload"]:
            self.process_code(self.current_activity["on_unload"])
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
