import time

from pynput import keyboard

from database.db import (
    insert_keystroke,
    insert_event
)

from utils.session import SESSION_ID

print(f"\nSession Started: {SESSION_ID}\n")

pressed_keys = {}


def on_press(key):
    try:
        key_data = key.char
    except AttributeError:
        key_data = str(key)

    pressed_keys[key_data] = time.time()

    insert_event(
        SESSION_ID,
        "key_press",
        {
            "key": key_data
        }
    )

    print(f"Pressed: {key_data}")


def on_release(key):
    try:
        key_data = key.char
    except AttributeError:
        key_data = str(key)

    if key_data in pressed_keys:

        press_time = pressed_keys[key_data]

        release_time = time.time()

        dwell_time = release_time - press_time

        insert_keystroke(
            SESSION_ID,
            key_data,
            press_time,
            release_time,
            dwell_time
        )

        insert_event(
            SESSION_ID,
            "key_release",
            {
                "key": key_data
            }
        )

        print(
            f"Released: {key_data} | "
            f"Dwell: {dwell_time:.4f}"
        )

        del pressed_keys[key_data]


def start_keyboard_listener():

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )

    listener.start()
    listener.join()