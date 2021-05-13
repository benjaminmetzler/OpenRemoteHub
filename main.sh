#!/bin/bash

cd /home/pi/my_remote
source /home/pi/my_remote/venv/bin/activate
sudo /home/pi/my_remote/venv/bin/python3 scripts/main.py
# sudo python3 scripts/keyboard_loop.py
