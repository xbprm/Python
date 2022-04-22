import os
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import json

TOGGLE_KEY = KeyCode(char="t")

clicking = False
repetition = 0.01
mouse = Controller()


def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
        global repetition
        time.sleep(repetition)


def toggle_event(key):
    if key == TOGGLE_KEY:
        global clicking
        clicking = not clicking


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as config_file:
        data = json.load(config_file)
        global repetition
        repetition = data["repetition"]


def main():
    read_config()

    click_thread = threading.Thread(target=clicker)
    click_thread.start()

    with Listener(on_press = toggle_event) as listener:
        listener.join()


if __name__ == "__main__":
    main()