# pylint: disable=C0116 C0114 C0115

import json
import os
import pathlib
import time
import threading
import queue
import lirc
import keyboard

# Main command queue for the MyRemote
lock = threading.Lock()
mainQueue = queue.Queue()
lirc_client = lirc.Client()


class MyDevice(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.device_queue = queue.Queue()
        self.stop = False

    def kill(self, force):
        if not force:
            # any additional commands will be ignored
            self.device_queue.put('{ "type":"kill"}')
        else:
            # stop after the next command
            self.stop = True

    def put(self, command):
        self.device_queue.put(command)

    def run(self):
        # the basic idea is that each device will handle it's
        # own queue sleeps, sending commands to the mainQueue for
        # processing the events at a system level.
        print("Starting " + self.name)
        while not self.stop:
            if not self.device_queue.empty():
                command = self.device_queue.get()
                if command["type"] == "sleep":
                    time.sleep(float(command["duration"]))
                elif command["type"] == "kill":
                    self.stop = True
                else:
                    with lock:
                        mainQueue.put(command)
                    # lock.release()


class MyRemote:
    def __init__(self, conf_file):
        self.mode = {}
        self.current_mode_file = ""
        self.key_presses = {}
        self.devices = {}
        threading.Thread(target=self.run).start()
        self.load(conf_file)

    def run(self):
        print("Starting MyRemote")

        while True:
            if not mainQueue.empty():
                with lock:
                    self.run_command(mainQueue.get())

    def run_command(self, code):
        repeat = 1
        if "repeat" in code:
            repeat = code["repeat"]

        if "type" in code:
            for _ in range(repeat):
                if code["type"] == "ir":
                    self.lirc(code["device"], code["code"])
                # elif code["type"] == "bluetooth":
                #     self.bluetooth(code["device"], code["code"])
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
                        self.run_command(macro_code)
                else:
                    print("Unknown type(%s)" % code["type"])

        else:
            print("Type not found: %s" % code)

    def assign_command(self, command):
        # assigns a command to a device queue
        # The device queue must already exist
        if "type" in command:
            if command["type"] == "macro":
                for macro_command in command["macro"]:
                    self.assign_command(macro_command)
            if command["type"] == "load":
                mainQueue.put(command)
            elif "device" in command:
                # Would it be better to parse through the json to find all
                # the devices to spin them up during load?  I tried this before
                # but the logic for getting all the devices in all the macros
                # proved difficult.  Instead I create the device queues on
                # the fly.
                if not command["device"] in self.devices:
                    self.devices[command["device"]] = MyDevice(command["device"])
                    self.devices[command["device"]].start()
                self.devices[command["device"]].put(command)
            else:
                print("Unable to parse command to correct queue (%s)" % command)
        else:
            print("Type not found: %s" % command)

    def load(self, conf_file):
        file = pathlib.Path(conf_file)
        if file.exists():

            self.on_unload()

            # tell the threads to finish processing
            # after the current commands have finished.
            for device in self.devices:
                self.devices[device].kill(False)

            # # wait for all devices to finish commands
            # for device in self.devices:
            #     print("Stopping %s thread" % device)
            #     self.devices[device].join()

            # read the common file
            with open("/home/pi/my_remote/json/common.json") as file:
                self.common = json.load(file)

            # read the specified configuration file
            with open(conf_file) as file:
                self.mode = json.load(file)

            # merge the common with the current mode file
            self.mode.update(self.common)

            self.current_mode_file = conf_file

            # load up the defaults for the mode file
            self.on_load()
        else:
            print("Unable to find: %s" % conf_file)

    @classmethod
    def lirc(cls, device, code):
        command = 'irsend SEND_ONCE "%s" "%s"' % (device, code)
        print("%s | %s" % (device, command))
        try:
            lirc_client.send_once(device, code)
        except lirc.exceptions.LircdCommandFailureError as error:
            print("Unable to send the %s key to %s!" % (device, code))
            print(error)  # Error has more info on what lircd sent back.

    @classmethod
    def adb(cls, device, code):
        if code == "CONNECT":
            command = "adb connect %s" % device
        elif code == "DISCONNECT":
            command = "adb disconnect"
        else:
            command = 'adb shell input keyevent "%s"' % code
        print("%s | %s" % (device, command))
        os.system(command)

    @classmethod
    def curl(cls, device, code):
        command = 'curl "%s" "%s"' % (code, device)
        print("%s | %s" % (device, command))
        os.system(command)

    # @classmethod
    # def bluetooth(self, device, code):
    #     command = "TBD: %s --> bluetooth(%s)" % (device, code)
    #     print("%s | %s" % (device, command))
    #     # os.system("TK")

    @classmethod
    def sleep(cls, device, duration):
        command = 'sleep "%s"' % duration
        print("%s | %s" % (device, command))
        os.system(command)

    def callback_key_release(self, event):
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
                if time_diff > 1 and "long_press" in self.mode[scan_code]:
                    self.assign_command(self.mode[scan_code]["long_press"])
                else:
                    self.assign_command(self.mode[scan_code])

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
            self.assign_command(self.mode["on_load"])

    def on_unload(self):
        print("on_unload: %s" % self.current_mode_file)
        if "on_unload" in self.mode:
            self.assign_command(self.mode["on_unload"])
        self.mode = {}

    def event_loop(self):
        keyboard.on_press(callback=self.callback_key_press, suppress=True)
        keyboard.on_release(callback=self.callback_key_release, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = MyRemote("/home/pi/my_remote/json/common.json")
    my_remote.event_loop()
