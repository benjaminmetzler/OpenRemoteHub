from evdev import InputDevice
from evdev.ecodes import EV_KEY
import threading
import time


class Keyboard:
    """main class"""

    def __init__(self, input_device_path, command_queue):
        self.input_device_path = input_device_path
        self.command_queue = command_queue
        self.long_press_limit = 1.0
        self.keyboard = InputDevice(self.input_device_path)

    def start(self):
        """start"""
        key_press_time = None
        long_press_timer = None  # new variable to track long press duration

        for event in self.keyboard.read_loop():
            # read_loop will return all types of input,
            # so we want to only look at keyboard presses
            if event.type == EV_KEY:
                if event.value == 1:
                    key_press_time = event.timestamp()
                    long_press_timer = threading.Timer(self.long_press_limit, self.handle_long_press, args=[event.code])
                    long_press_timer.start()
                elif event.value == 0:
                    if key_press_time is not None:
                        key_release_time = event.timestamp()
                        time_elapsed = key_release_time - key_press_time
                        long_press_timer.cancel()  # release detected, cancel the long press timer
                        if time_elapsed < self.long_press_limit:
                            self.command_queue.put({"scancode": event.code, "long_press": False})
                    key_press_time = None
                    long_press_timer = None

    def handle_long_press(self, code, long_press=True):
        """handle long press"""
        self.command_queue.put({"scancode": code, "long_press": long_press})

    def stop(self):
        """stop"""
        self.keyboard.close()
