from pynput import mouse
import uuid

import time
from database.db import insert_event

print("mouse_listener imported")

session_id = str(uuid.uuid4())[:8]



last_move_time = 0


def on_move(x, y):
    global last_move_time

    current_time = time.time()

    if current_time - last_move_time < 0.1:
        return

    last_move_time = current_time

    insert_event(
        session_id,
        "mouse_move",
        {
            "x": x,
            "y": y
        }
    )


def on_click(x, y, button, pressed):
    print(f"CLICK: {x}, {y}")

    insert_event(
        session_id,
        "mouse_click",
        {
            "x": x,
            "y": y,
            "button": str(button),
            "pressed": pressed
        }
    )


def start_mouse_listener():

    print("Starting mouse listener...")
    print("Press ENTER to stop.\n")

    listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click
    )

    listener.start()

    input()

    listener.stop()

    print("Mouse listener stopped.")