import struct
from jsonc_parser.parser import JsoncParser

f = open("/dev/input/event0", "rb")
# Open the file in the read-binary mode

file_path = "../documentation/default_keys.jsonc"
buttons = JsoncParser.parse_file(file_path)

for button in buttons:
    print("Press button to map to the %s or hit enter to skip" % buttons[button])

    # Capture the button down
    data = f.read(24)

    # only capture the hex value of the keypres
    key_value = "KEY_%s" % (hex(struct.unpack("4IHHI", data)[3])[2:])

    # Discard the SYNs and button up presses
    f.read(24)  # Button down SYN
    f.read(24)  # Button up
    f.read(24)  # Button up SYN

    print(key_value)
