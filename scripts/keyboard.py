""" keyboard.py """
import threading
from evdev import InputDevice
from evdev.ecodes import EV_KEY


class Keyboard:
    """Main class representing a keyboard input handler."""

    def __init__(self, input_device_path, command_queue):
        """Initialize the Keyboard instance with the provided
        input device path and command queue."""
        self.input_device_path = input_device_path
        self.command_queue = command_queue
        self.long_press_limit = (
            1.0  # Time threshold to consider a keypress as a long press
        )
        self.keyboard = InputDevice(
            self.input_device_path
        )  # Create an InputDevice instance for the specified keyboard

    def start(self):
        """Start method to read keyboard events and handle key presses."""
        key_press_time = None
        long_press_timer = None

        for event in self.keyboard.read_loop():
            # read_loop will return all types of input, so we only look at keyboard presses
            if event.type == EV_KEY:
                if event.value == 1:  # Key press event
                    key_press_time = event.timestamp()
                    # Set up a timer for long press detection
                    long_press_timer = threading.Timer(
                        self.long_press_limit, self.handle_long_press, args=[event.code]
                    )
                    long_press_timer.start()
                elif event.value == 0:  # Key release event
                    if key_press_time is not None:
                        key_release_time = event.timestamp()
                        time_elapsed = key_release_time - key_press_time
                        # If a long press timer is active, cancel it
                        if long_press_timer and long_press_timer.is_alive():
                            long_press_timer.cancel()
                        # Check if the key press duration is less than the long press threshold
                        # and enqueue the corresponding command to the command queue
                        if time_elapsed < self.long_press_limit:
                            self.command_queue.put(
                                {"scancode": event.code, "long_press": False}
                            )
                    key_press_time = None
                    long_press_timer = None

    def handle_long_press(self, code, long_press=True):
        """Handle long press events by enqueueing the corresponding
        command to the command queue."""
        self.command_queue.put({"scancode": code, "long_press": long_press})

    def stop(self):
        """Stop method to close the keyboard input device."""
        self.keyboard.close()
