""" main.py """
import queue
import threading
import os
from keyboard import Keyboard
from command_processor import CommandProcessor

if __name__ == "__main__":

    # Creating a queue for communication between the Keyboard
    # and CommandProcessor threads.
    command_queue = queue.Queue()

    # Creating an instance of the CommandProcessor class with a command queue,
    # configuration file path, plugin directory, and timeout value.
    command_processor = CommandProcessor(
        command_queue, "json/common.json", "scripts/plugins", 60
    )

    # Creating an instance of the Keyboard class with the keyboard device
    # path and the command queue.
    default_keyboard = os.getenv("OPEN_REMOTE_HUB_KEYBOARD", "/dev/input/event0")
    keyboard = Keyboard(default_keyboard, command_queue)

    # Creating threads for the keyboard and command processor to run concurrently.
    keyboard_thread = threading.Thread(target=keyboard.start)
    command_processor_thread = threading.Thread(target=command_processor.start)

    # Starting the threads to execute the start methods of the Keyboard and
    # CommandProcessor instances.
    keyboard_thread.start()
    command_processor_thread.start()

    # Waiting for the threads to complete their execution.
    # Note, they will not exit on their own.
    keyboard_thread.join()
    command_processor_thread.join()
