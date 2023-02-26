import keyboard


class OpenRemoteHub:
    def __init__(self):
        print("waiting for keystroke")

    def callback(self, event):
        scan_code = event.scan_code
        name = event.name
        print(f"{scan_code}({name}")

    def start(self):
        keyboard.on_release(callback=self.callback, suppress=True)
        keyboard.wait()


if __name__ == "__main__":
    OpenRemoteHub = OpenRemoteHub()
    OpenRemoteHub.start()
