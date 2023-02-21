""" Handle keyboard events and push them to the command queue """
from evdev import InputDevice
from evdev.ecodes import EV_KEY


class Keyboard:
    """main class"""

    def __init__(self, input_device_path, command_queue):
        self.input_device_path = input_device_path
        self.command_queue = command_queue
        self.long_press_limit = 0.75
        self.keyboard = InputDevice(self.input_device_path)

    def start(self):
        """start"""
        key_press_time = None
        key_release_time = None

        for event in self.keyboard.read_loop():
            # read_loop will return all types of input,
            # so we want to only look at keyboard presses
            if event.type == EV_KEY:
                if event.value == 1:
                    key_press_time = event.timestamp()
                elif event.value == 0:
                    key_release_time = event.timestamp()
                    if key_press_time is not None:
                        time_elapsed = key_release_time - key_press_time
                        command = {"scancode": event.code, "time_elapsed": time_elapsed}
                        self.command_queue.put(command)

                        # Read and ignore the next event to discard the key press
                        try:
                            self.keyboard.read_one()
                        except OSError as error:
                            # handle I/O error or device disconnection
                            print("Error reading from keyboard device:", error)
                        except ValueError as error:
                            # handle invalid input data
                            print("Invalid input event:", error)

                    key_press_time = None
                    key_release_time = None

    def stop(self):
        """stop"""
        self.keyboard.close()
