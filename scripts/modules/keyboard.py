# keyboard.py
from evdev import InputDevice, ecodes

class Keyboard:
    def __init__(self, input_device_path, command_queue):
        self.input_device_path = input_device_path
        self.command_queue = command_queue
        self.long_press_limit = 0.75
        self.keyboard = InputDevice(self.input_device_path)

    def start(self):
        key_press_time = None
        key_release_time = None

        for event in self.keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    key_press_time = event.timestamp()
                elif event.value == 0:
                    key_release_time = event.timestamp()
                    if key_press_time is not None:
                        time_elapsed = key_release_time - key_press_time
                        command = {"code": event.code, "time_elapsed": time_elapsed}
                        self.command_queue.put(command)

                        # Read and ignore the next event to discard the key press
                        try:
                            self.keyboard.read_one()
                        except OSError as e:
                            # handle I/O error or device disconnection
                            print("Error reading from keyboard device:", e)
                        except ValueError as e:
                            # handle invalid input data
                            print("Invalid input event:", e)

                    key_press_time = None
                    key_release_time = None

    def stop(self):
        self.keyboard.close()
