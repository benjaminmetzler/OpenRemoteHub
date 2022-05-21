'''my_remote'''
import json
import os
import pathlib
import time
import keyboard
import lirc


class My_Remote:
    '''my_remote'''
    def __init__(self, conf_file):
        '''__init__(self, conf_file):'''
        self.mode = {}
        self.current_mode_file = ""
        self.load(conf_file)
        self.key_presses = {}
        self.client = lirc.Client()

    # @staticmethod
    def process_code(self, code, long_press): # pylint: disable=too-many-branches
        '''process_code(self, code, long_press):'''
        if long_press and "long_press" in code:
            code = code["long_press"]
        if "type" in code:
            if "repeat" in code:
                repeat = code["repeat"]
            else:
                repeat = 1
            for repeat_count in range(repeat):
                print(f"Try {repeat_count}")
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
                elif code["type"] == "appletv":
                    self.appletv(code["device"], code["code"])
                else:
                    print(f'Unknown type({code["type"]})')

        else:
            print(f"Type not found: {code}" )

    # @staticmethod
    def load(self, conf_file):
        '''load(self, conf_file):'''
        file = pathlib.Path(conf_file)
        if file.exists():

            self.on_unload()

            # read the common file
            # TK should we have an on_load and on_unload in the common.json?
            # TK how should they be handled?
            with open("/home/pi/my_remote/json/common.json", "r", encoding="utf8") as file_handle:
                self.common = json.load(file_handle)


            # read the configuration file
            with open(conf_file, "r", encoding="utf8") as file_handle:
                self.mode = json.load(file_handle)

            self.mode.update(self.common)

            self.current_mode_file = conf_file
            # load up the defaults
            self.on_load()
        else:
            print(f"Unable to find: {conf_file}")

    # @staticmethod
    def send_ir(self, device, code):
        '''send_ir(self, device, code):'''
        # command = f'irsend SEND_ONCE "{device}" "{code}"'
        print(f"{device} | {code}")
        try:
            self.client.send_once(device, code)
        except lirc.exceptions.LircdCommandFailureError as error:
            print(f"Unable to send the {device} key to {code}!")
            print(error)  # Error has more info on what lircd sent back.
            # os.system(command)

    # @staticmethod
    def adb(self, device, code):
        '''adb(self, device, code):'''
        if code == "CONNECT":
            command = f"adb connect {device}"
        elif code == "DISCONNECT":
            command = "adb disconnect"
        else:
            command = f'adb shell input keyevent "{code}"'
        print(f"{device} | {code}")
        os.system(command)

    # @staticmethod
    def appletv(self, device, code):
        '''appletv(self, device, code):'''
        command = f"TBD: {device} --> AppleTV({code})"
        print(f"{device} | {command}")

    # @staticmethod
    def curl(self, device, code):
        '''curl(self, device, code):'''
        command = f'curl "{code}" "{device}"'
        print(f"{device} | {code}")
        os.system(command)

    # @staticmethod
    def bluetooth(self, device, code):
        '''bluetooth(self, device, code):'''
        command = f"TBD: {device} --> bluetooth({code})"
        print(f"{device} | {command}")
        # os.system("TK")

    # @staticmethod
    def sleep(self, device, duration):
        '''sleep(self, device, duration):'''
        command = f'sleep "{duration}"'
        print(f"{device} | {command}")
        os.system(command)

    # @staticmethod
    def callback_key_release(self, event):
        '''callback_key_release(self, event):'''
        long_press = False
        scan_code = str(event.scan_code)
        name = event.name
        print(f"callback_key_release: {event} - {scan_code} ({name})" )
        if scan_code in self.mode:
            if scan_code in self.key_presses:
                current_time = time.time()
                time_diff = current_time - self.key_presses[scan_code]
                del self.key_presses[scan_code]
                print(f"key_press_duration={time_diff}")

                # NOTE: If the time of a keypress is greater than 1 second
                # then handle this as a long press
                if time_diff > 1:
                    long_press = True

                self.process_code(self.mode[scan_code], long_press)

    # @staticmethod
    def callback_key_press(self, event):
        '''callback_key_press(self, event):'''
        # This callback adds the keypress to the dictionary along
        # with the current time so that when the key is released
        # the time can be used to determine if it was a long
        # or short press, allowing different actions for the same key.
        scan_code = str(event.scan_code)
        name = event.name
        print(f"callback_key_press: {event} - {scan_code} ({name})")
        if scan_code in self.mode:
            if scan_code not in self.key_presses:
                self.key_presses[scan_code] = time.time()
            print(self.key_presses)

    # @staticmethod
    def on_load(self):
        '''on_load(self):'''
        print(f"on_load: {self.current_mode_file}")
        if "on_load" in self.mode:
            self.process_code(self.mode["on_load"], False)

    # @staticmethod
    def on_unload(self):
        '''on_unload(self):'''
        print(f"on_unload: {self.current_mode_file}")
        if "on_unload" in self.mode:
            self.process_code(self.mode["on_unload"], False)
        self.mode = {}

    # @staticmethod
    def event_loop(self):
        '''event_loop(self):'''
        keyboard.on_press(callback=self.callback_key_press, suppress=True)
        keyboard.on_release(callback=self.callback_key_release, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote("/home/pi/my_remote/json/common.json")
    my_remote.event_loop()
