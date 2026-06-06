import time

import win32gui
import win32process
import psutil

from database.db import insert_event
from utils.session import SESSION_ID


def get_active_app():
    hwnd = win32gui.GetForegroundWindow()

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        return psutil.Process(pid).name()
    except Exception:
        return "unknown"


def start_app_switch_tracker():

    previous_app = None

    print("App switch tracker started")
    print("Press Ctrl+C to stop\n")

    while True:

        current_app = get_active_app()

        if current_app != previous_app:

            print(f"Switched to: {current_app}")

            insert_event(
                SESSION_ID,
                "focus_change",
                {
                    "app": current_app
                }
            )

            previous_app = current_app

        time.sleep(1)