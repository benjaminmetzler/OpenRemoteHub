import json
import keyboard
import os
import pathlib
import time
import lirc


class My_Remote:
    def __init__(self, conf_file):
        self.mode = {}
        self.current_mode_file = ""
        self.load(conf_file)
        self.key_presses = {}
        self.client = lirc.Client()

    def process_code(self, code, long_press):
        if long_press and "long_press" in code:
            code = code["long_press"]
        if "type" in code:
            if "repeat" in code:
                repeat = code["repeat"]
            else:
                repeat = 1
            for x in range(repeat):
                if code["type"] == "ir":
                    self.send_ir(code["device"], code["code"])
                elif code["type"] == "bluetooth":
                    self.bluetooth(code["device"], code["code"])
                elif code["type"] == "adb":
                    self.adb(code["device"], code["code"])
                elif code["type"] == "curl":
                    self.curl(code["device"], code["code"])
                elif code["type"] == "load":
                    self.load(code["file"])
                elif code["type"] == "sleep":
                    self.sleep(code["device"], code["duration"])
                elif code["type"] == "macro":
                    for macro_code in code["macro"]:
                        self.process_code(macro_code, long_press)
                else:
                    print("Unknown type(%s)" % self.code["type"])

        else:
            print("Type not found: %s" % code)

    def load(self, conf_file):
        file = pathlib.Path(conf_file)
        if file.exists():

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

            self.mode.update(self.common)

            self.current_mode_file = conf_file
            # load up the defaults
            self.on_load()
        else:
            print("Unable to find: %s" % conf_file)

    def send_ir(self, device, code):
        command = 'irsend SEND_ONCE "%s" "%s"' % (device, code)
        print("%s | %s" % (device, command))
        try:
            self.client.send_once(device, code)
        except lirc.exceptions.LircdCommandFailureError as error:
            print("Unable to send the %s key to %s!" % (device, code))
            print(error)  # Error has more info on what lircd sent back.
            # os.system(command)

    def adb(self, device, code):
        if code == "CONNECT":
            command = "adb connect %s" % device
        elif code == "DISCONNECT":
            command = "adb disconnect"
        else:
            command = 'adb shell input keyevent "%s"' % code
        print("%s | %s" % (device, command))
        os.system(command)

    def curl(self, device, code):
        command = 'curl "%s" "%s"' % (code, device)
        print("%s | %s" % (device, command))
        os.system(command)

    def bluetooth(self, device, code):
        command = "TBD: %s --> bluetooth(%s)" % (device, code)
        print("%s | %s" % (device, command))
        # os.system("TK")

    def sleep(self, device, duration):
        command = 'sleep "%s"' % duration
        print("%s | %s" % (device, command))
        os.system(command)

    def callback_key_release(self, event):
        long_press = False
        scan_code = str(event.scan_code)
        name = event.name
        print("callback_key_release: %s - %s (%s)" % (event, scan_code, name))
        if scan_code in self.mode:
            if scan_code in self.key_presses:
                current_time = time.time()
                time_diff = current_time - self.key_presses[scan_code]
                del self.key_presses[scan_code]
                print("key_press_duration=%s" % time_diff)

                # NOTE: If the time of a keypress is greater than 1 second
                # then handle this as a long press
                if time_diff > 1:
                    long_press = True

                self.process_code(self.mode[scan_code], long_press)

    def callback_key_press(self, event):
        # This callback adds the keypress to the dictionary along
        # with the current time so that when the key is released
        # the time can be used to determine if it was a long
        # or short press, allowing different actions for the same key.
        scan_code = str(event.scan_code)
        name = event.name
        print("callback_key_press: %s - %s (%s)" % (event, scan_code, name))
        if scan_code in self.mode:
            if scan_code not in self.key_presses:
                self.key_presses[scan_code] = time.time()
            print(self.key_presses)

    def on_load(self):
        print("on_load: %s" % self.current_mode_file)
        if "on_load" in self.mode:
            self.process_code(self.mode["on_load"], False)

    def on_unload(self):
        print("on_unload: %s" % self.current_mode_file)
        if "on_unload" in self.mode:
            self.process_code(self.mode["on_unload"], False)
        self.mode = {}

    def event_loop(self):
        keyboard.on_press(callback=self.callback_key_press, suppress=True)
        keyboard.on_release(callback=self.callback_key_release, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote("/home/pi/my_remote/json/common.json")
    my_remote.event_loop()
