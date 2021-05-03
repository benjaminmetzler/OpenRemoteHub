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


# read the common file
f = open("/home/pi/my_remote/test_scripts/common.json")
common = json.load(f)
f.close()

# read the configuration file
f = open(conf_file)
mode = json.load(f)
f.close()

