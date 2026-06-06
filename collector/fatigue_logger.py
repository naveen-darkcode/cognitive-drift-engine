from database.db import insert_fatigue_label
from utils.session import SESSION_ID


def start_fatigue_logger():

    while True:

        try:

            fatigue_level = int(
                input(
                    "\nEnter fatigue level (1-10): "
                )
            )

            if fatigue_level < 1 or fatigue_level > 10:
                print("Please enter a value between 1 and 10")
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
            print("Enter a valid number")