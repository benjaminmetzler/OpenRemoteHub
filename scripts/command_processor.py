""" command_processor.py """
import pathlib
import json
import time
import importlib.util
import threading


class CommandProcessor:
    """Class for processing commands based on input events."""

    def __init__(
        self,
        command_queue,
        activity_file,
        plugin_dir=None,
        plugin_refresh_interval=None,
    ):
        """Initialize CommandProcessor with necessary parameters."""

        # Initialize instance variables
        self.command_queue = command_queue
        self.current_activity_file = activity_file
        self.current_activity = {}
        self.plugins = {}
        self.plugins_lock = threading.Lock()
        self.plugin_dir = plugin_dir
        self.plugin_refresh_interval = (
            plugin_refresh_interval or 3600
        )  # default to 1 hour
        # Load plugins and configuration file
        self.load_plugins()
        self.load_conf_file(self.current_activity_file)

    def load_plugins_periodically(self):
        """Periodically load plugins in a separate thread."""

        while True:
            self.load_plugins()
            time.sleep(self.plugin_refresh_interval)

    def start(self):
        """Start method to process commands based on input events."""

        # Start a separate thread to periodically load plugins
        reload_thread = threading.Thread(
            target=self.load_plugins_periodically, daemon=True
        )
        reload_thread.start()

        while True:

            # Get the next command from the command queue
            item = self.command_queue.get()
            scancode = str(item["scancode"])
            long_press = item["long_press"]
            print(f"processing scancode {scancode}, long_press {long_press}")

            # Process the command based on the current activity configuration
            if scancode in self.current_activity:
                code = self.current_activity[scancode]
                if long_press and "long_press" in code:
                    code = code["long_press"]
                with self.plugins_lock:
                    self.process_code(code)
            else:
                print(f"scancode {scancode} not found")

            self.command_queue.task_done()

    def process_code(self, code: str):
        """Process the provided code according to its defined action."""

        # Repeat the indicated action based on the number
        # of repeats requested, defaulting to 1.
        for _ in range(code.get("repeat", 1)):
            action = code["action"]
            if action == "load":
                self.load_conf_file(code["file"])
            elif action == "sleep":
                self.sleep(code["device"], code["duration"])
            elif action == "macro":
                print(f"MACRO: {code})")
                for macro_code in code["macro"]:
                    self.process_code(macro_code)
            elif action in self.plugins:
                self.plugins[action](code)
            else:
                print(f"Unknown action({action})")

    def register_plugin(self, action, plugin_func):
        """Register a plugin action and its corresponding function."""
        self.plugins[action] = plugin_func

    def load_plugins(self):
        """Load plugins from the specified directory."""
        if not self.plugin_dir:
            return

        path = pathlib.Path(self.plugin_dir)
        if not path.is_dir():
            return

        with self.plugins_lock:
            for plugin_file in path.glob("*.py"):
                plugin_name = plugin_file.stem
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)
                action = plugin_file.stem
                self.register_plugin(action, plugin_module.run)

    def sleep(self, device, duration):
        """Pause execution for the specified duration."""
        print(f"SLEEP: {device}, {duration}")
        time.sleep(float(duration))

    def on_load(self):
        """Handle actions specified in the 'on_load' section of the configuration."""
        print(f"on_load: {self.current_activity_file}")
        if "on_load" in self.current_activity and self.current_activity["on_load"]:
            self.process_code(self.current_activity["on_load"])

    def on_unload(self):
        """Handle actions specified in the 'on_unload' section of the configuration."""
        print(f"on_unload: {self.current_activity_file}")
        if "on_unload" in self.current_activity and self.current_activity["on_unload"]:
            self.process_code(self.current_activity["on_unload"])
        self.current_activity = {}

    def load_conf_file(self, conf_file: str):
        """Load and process the specified configuration file."""
        file = pathlib.Path(conf_file)
        if file.exists():
            self.on_unload()

            # Read the common file
            with open("json/common.json", encoding="utf-8") as file:
                common = json.load(file)

            # Read the configuration file
            with open(conf_file, encoding="utf-8") as file:
                self.current_activity = json.load(file)

            self.current_activity.update(common)
            self.current_activity_file = conf_file
            self.on_load()
        else:
            print(f"Unable to find: {conf_file}")
