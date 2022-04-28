import os
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import json

TOGGLE_KEY = KeyCode(char="c")
TOGGLE_KEY_MULTI = KeyCode(char="m")

enabled = False
enabled_multi = False
locations = []
location_names = []
location = 0
location_name = []
repetition = 0.01
mouse = Controller()


def clicker():
    while True:
        if enabled:
            mouse.click(Button.left, 1)
            if enabled_multi:
                global locations
                global location_names
                global location     
                global location_name
               
                location = (location + 1) % len(location_names)
                location_name = location_names[location]
                mouse.position = (locations[location_name]["x"], locations[location_name]["y"])
        global repetition
        time.sleep(repetition)


def toggle_event(key):
    global enabled
    if key == TOGGLE_KEY:
        enabled = not enabled
    if key == TOGGLE_KEY_MULTI:
        enabled = not enabled
        global enabled_multi
        enabled_multi = not enabled_multi


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as config_file:
        data = json.load(config_file)
        computername = os.environ.get("COMPUTERNAME")
        global repetition
        repetition = float(data["repetition"][computername])
        global locations
        locations = data["locations"][computername]
        global location_names
        location_names = data["location_names"][computername]
        

def main():
    read_config()

    click_thread = threading.Thread(target=clicker)
    click_thread.start()

    with Listener(on_press = toggle_event) as listener:
        listener.join()


if __name__ == "__main__":
    main()