import uuid
import time

from pynput import keyboard

from database.db import insert_keystroke

session_id = str(uuid.uuid4())[:8]

print(f"\nSession Started: {session_id}\n")

pressed_keys = {}

def on_press(key):
    try:
        key_data = key.char
    except AttributeError:
        key_data = str(key)

    pressed_keys[key_data] = time.time()

    print(f"Pressed: {key_data}")

def on_release(key):
    try:
        key_data = key.char
    except AttributeError:
        key_data = str(key)

    if key_data in pressed_keys:

        press_time = pressed_keys[key_data]

        release_time = time.time()

        dwell_time = (
            release_time - press_time
        )

        print(
            f"Released: {key_data} | "
            f"Dwell: {dwell_time:.4f}"
        )

        insert_keystroke(
            session_id,
            key_data,
            press_time,
            release_time,
            dwell_time
        )

        del pressed_keys[key_data]

def start_keyboard_listener():

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )

    listener.start()

    listener.join()