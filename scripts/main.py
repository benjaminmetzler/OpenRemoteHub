import queue
import threading
from keyboard import Keyboard
from command_processor import CommandProcessor

if __name__ == "__main__":
    command_queue = queue.Queue()

    command_processor = CommandProcessor(command_queue, "json/common.json")
    keyboard = Keyboard("/dev/input/event0", command_queue)

    keyboard_thread = threading.Thread(target=keyboard.start)
    command_processor_thread = threading.Thread(target=command_processor.start)

    keyboard_thread.start()
    command_processor_thread.start()

    keyboard_thread.join()
    command_processor_thread.join()
