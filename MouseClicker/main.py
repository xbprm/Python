import os
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import json

TOGGLE_KEY = KeyCode(char="m")

enabled = False
locations = []
position = 0
repetition = 0.01
mouse = Controller()


def clicker():
    while True:
        if enabled:
            global locations
            global position            
            mouse.position = locations[position]
            mouse.click(Button.left, 1)
            position = (position + 1) % len(locations)
        global repetition
        time.sleep(repetition)


def toggle_event(key):
    if key == TOGGLE_KEY:
        global enabled
        enabled = not enabled
        invert = False


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as config_file:
        data = json.load(config_file)
        global repetition
        repetition = data["repetition"]
        global locations
        locations = data["locations"]
        

def main():
    read_config()

    click_thread = threading.Thread(target=clicker)
    click_thread.start()

    with Listener(on_press = toggle_event) as listener:
        listener.join()


if __name__ == "__main__":
    main()