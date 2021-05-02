from pynput.keyboard import Listener


def on_press(key):
    print(str(key))


def on_release(key):
    pass


listener_thread = Listener(on_press=on_press, on_release=None)
# This is a daemon=True thread, use .join() to prevent code from exiting  
listener_thread.start()