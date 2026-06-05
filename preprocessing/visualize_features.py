import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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

    return total_keys / total_time

def calculate_latency(window):
    press_times = window["press_time"].tolist()

    latencies = []

    for i in range(1, len(press_times)):
        latencies.append(
            press_times[i]
            - press_times[i - 1]
        )

    if len(latencies) == 0:
        return 0

    return sum(latencies) / len(latencies)

def generate_feature_series(df):

    typing_speeds = []
    latencies = []
    windows = []

    count = 1

    for start in range(0, len(df), WINDOW_SIZE):

        end = start + WINDOW_SIZE

        window = df.iloc[start:end]

        if len(window) < WINDOW_SIZE:
            continue

        typing_speeds.append(
            calculate_typing_speed(window)
        )

        latencies.append(
            calculate_latency(window)
        )

        windows.append(count)

        count += 1

    return windows, typing_speeds, latencies

def plot_features(
    windows,
    typing_speeds,
    latencies
):
    plt.figure(figsize=(10, 5))

    plt.plot(
        windows,
        typing_speeds,
        marker='o',
        label='Typing Speed'
    )

    plt.plot(
        windows,
        latencies,
        marker='o',
        label='Inter-Key Latency'
    )

    plt.xlabel("Window Number")

    plt.ylabel("Feature Value")

    plt.title(
        "Behavioral Drift Across Session"
    )

    plt.legend()

    plt.grid(True)

    plt.show()

def main():
    session_id = input("Enter Session ID: ")

    df = load_session_data(session_id)

    if df.empty:
        print("No data found.")
        return

    (
        windows,
        typing_speeds,
        latencies
    ) = generate_feature_series(df)

    plot_features(
        windows,
        typing_speeds,
        latencies
    )

if __name__ == "__main__":
    main()
    