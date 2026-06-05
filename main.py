from database.db import create_table
from collector.keyboard_listener import start_keyboard_listener

def main():
    print("\n===== Cognitive Drift Engine =====")
    print("Starting application...")

    # Create database table
    create_table()

    print("Database ready.")
    print("Keyboard listener started...")
    print("Press CTRL + C to stop.\n")

    try:
        # Start listener
        start_keyboard_listener()

    except KeyboardInterrupt:
        print("\nApplication stopped by user.")

    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main()