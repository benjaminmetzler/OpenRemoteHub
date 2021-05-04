import keyboard


class My_Remote:
    def __init__(self):
        print("waiting for keystroke")

    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        print("%s(%s)" % (scan_code, name))

    def start(self):
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    my_remote = My_Remote()
    my_remote.start()
