"""ir.py"""

import lirc


def run(code):
    """Send IR signal to device"""
    if "device" not in code:
        print("Missing 'device' key in IR plugin configuration")
        return

    if "code" not in code:
        print("Missing 'code' key in IR plugin configuration")
        return

    client = lirc.Client()
    device = code["device"]
    ir_code = code["code"]
    try:
        client.send_once(device, ir_code)
        print(f"IR: Sent '{ir_code}' to '{device}'")
    except lirc.exceptions.LircdCommandFailureError as error:
        print(f"IR: Unable to send '{ir_code}' to '{device}'")
        print(error)
