import json
import keyboard 
import os
from jsonmerge import merge


class My_Remote:
    def __init__(self, conf_file):
        
        # read the common file
        f = open("/home/pi/my_remote/test_scripts/common.json")
        self.common = json.load(f)
        f.close()

        # read the configuration file
        f = open(conf_file)
        self.mode = json.load(f)
        f.close()

    def send_code(self, name):
        if(name in self.mode):
            if self.mode[name]['type'] == "ir":
                self.send_ir( self.mode[name]['device'], self.mode[name]['code'])
            if self.mode[name]['type'] == "rf":
                self.send_rf( self.mode[name]['device'], self.mode[name]['code'])

    def send_ir(self, device, code):
        print(" %s --> send_ir(%s)" % (device, code))
        # TK sanitize parameters since we are running as root
        os.system("irsend SEND_ONCE %s %s" % (device, code))

    def send_rf(self, device, code):
        print(" %s --> send_ir(%s)" % (device, code))
        # TK sanitize parameters since we are running as root
        # os.system("irsend SEND_ONCE %s %s" % (device, code))

    def delay(self, device, timeout):
        print(" %s --> delay(%s)" % (device, timeout))
        
    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        self.send_code( name )
            
    def on_load(self):
        print("on_load")
        # on load
        # currently serial, but ideally parallelized so that multiple
        # codes could be sent across different devices, with each 
        # device getting it's own queue that can push to a single queue
        # that is then sent out the IR/RF hardware.
        if("on_load" in self.mode):
            for device in self.mode['on_load']:
                for code_entry in device['codes']:
                    if "code" in code_entry:
                        self.send_code( cane)
                    if "delay" in code_entry:
                        self.delay( device['device'], code_entry["delay"])

    def start(self):
        self.on_load()
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote('/home/pi/my_remote/documentation/sample.json')
    my_remote.start()
