import sqlite3
import pandas as pd

DB_NAME = "database/fatigue_logs.db"

WINDOW_SIZE = 20

def load_session_data(session_id):
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT * FROM keystrokes
    WHERE session_id = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(session_id,)
    )

    conn.close()

    return df

def calculate_typing_speed(window):
    total_keys = len(window)

    if total_keys < 2:
        return 0

    total_time = (
        window["release_time"].iloc[-1]
        - window["press_time"].iloc[0]
    ) / 60

    if total_time == 0:
        return 0

    return round(total_keys / total_time, 2)

def calculate_backspace_ratio(window):
    backspaces = window[
        window["key"] == "Key.backspace"
    ]

    total_keys = len(window)

    if total_keys == 0:
        return 0

    return round(
        len(backspaces) / total_keys,
        4
    )

def calculate_latency(window):
    press_times = window["press_time"].tolist()

    latencies = []

    for i in range(1, len(press_times)):
        latency = (
            press_times[i]
            - press_times[i - 1]
        )

        latencies.append(latency)

    if len(latencies) == 0:
        return 0

    return round(
        sum(latencies) / len(latencies),
        4
    )

def analyze_windows(df):
    print("\n===== Rolling Window Analysis =====\n")

    for start in range(0, len(df), WINDOW_SIZE):

        end = start + WINDOW_SIZE

        window = df.iloc[start:end]

        if len(window) < WINDOW_SIZE:
            continue

        typing_speed = calculate_typing_speed(window)

        backspace_ratio = calculate_backspace_ratio(window)

        latency = calculate_latency(window)

        print(f"Window {start//WINDOW_SIZE + 1}")

        print(f"Typing Speed: {typing_speed}")

        print(f"Backspace Ratio: {backspace_ratio}")

        print(f"Latency: {latency}")

        print("-" * 40)

def main():
    session_id = input("Enter Session ID: ")

    df = load_session_data(session_id)

    if df.empty:
        print("No data found.")
        return

    analyze_windows(df)

if __name__ == "__main__":
    main()