from pynput import mouse
import time

from database.db import insert_event
from utils.session import SESSION_ID

print("mouse_listener imported")

last_move_time = 0


def on_move(x, y):
    global last_move_time

    current_time = time.time()

    if current_time - last_move_time < 0.1:
        return

    last_move_time = current_time

    insert_event(
        SESSION_ID,
        "mouse_move",
        {
            "x": x,
            "y": y
        }
    )


def on_click(x, y, button, pressed):
    print(f"CLICK: {x}, {y}")

    insert_event(
        SESSION_ID,
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