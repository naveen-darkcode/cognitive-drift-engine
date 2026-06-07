import threading

from database.db import (
    create_table,
    insert_fatigue_label
)

from collector.keyboard_listener import (
    start_keyboard_listener
)

from collector.mouse_listener import (
    start_mouse_listener
)

from collector.app_switch_tracker import (
    start_app_switch_tracker
)

from utils.session import SESSION_ID


def start_keyboard():
    start_keyboard_listener()


def start_mouse():
    start_mouse_listener()


def start_app_tracker():
    start_app_switch_tracker()


def save_fatigue_label():

    while True:

        try:

            fatigue_level = int(
                input(
                    "\nEnter fatigue level (1-10): "
                )
            )

            if fatigue_level < 1 or fatigue_level > 10:

                print(
                    "Please enter a value between 1 and 10"
                )

                continue

            insert_fatigue_label(
                SESSION_ID,
                fatigue_level
            )

            print(
                f"Saved fatigue level: {fatigue_level}"
            )

            break

        except ValueError:

            print(
                "Enter a valid number"
            )


def main():

    create_table()

    print(
        "\n=== Cognitive Drift Collection Started ===\n"
    )

    print(
        f"SESSION ID: {SESSION_ID}\n"
    )

    keyboard_thread = threading.Thread(
        target=start_keyboard,
        daemon=True
    )

    mouse_thread = threading.Thread(
        target=start_mouse,
        daemon=True
    )

    app_thread = threading.Thread(
        target=start_app_tracker,
        daemon=True
    )

    keyboard_thread.start()
    mouse_thread.start()
    app_thread.start()

    print("Keyboard Tracker Running")
    print("Mouse Tracker Running")
    print("App Switch Tracker Running")

    print(
        "\nCollect data for a few minutes."
    )

    print(
        "Press ENTER when finished.\n"
    )

    input()

    save_fatigue_label()

    print(
        "\nSession completed successfully."
    )


if __name__ == "__main__":
    main()