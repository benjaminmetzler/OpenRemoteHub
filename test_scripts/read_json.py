import json
import time
import keyboard


class MR_Configuration:
    def __init__(self, conf_file):
        self.conf_file = conf_file


def send_code(device, code):
    print(" %s --> send_code(%s)" % (device, code))


def sleep(device, timeout):
    print(" %s --> sleep(%s)" % (device, timeout))


with open("/Users/ben/Projects/my_remote/documentation/sample.json") as f:
    mode = json.load(f)

# on load
# currently serial, but ideally parallelized so that multiple
# codes could be sent across different devices, with each
# device getting it's own queue that can push to a single queue
# that is then sent out the IR/RF hardware.
for device in mode["on_load"]:
    for code_entry in device["codes"]:
        if "code" in code_entry:
            send_code(device["device"], code_entry["code"])
        if "sleep" in code_entry:
            sleep(device["device"], code_entry["sleep"])
