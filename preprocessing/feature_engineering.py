import sqlite3
import pandas as pd

DB_NAME = "database/fatigue_logs.db"

def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = "SELECT * FROM keystrokes"

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

def calculate_typing_speed(df):
    total_keys = len(df)

    if total_keys < 2:
        return 0

    total_time = (
        df["release_time"].iloc[-1]
        - df["press_time"].iloc[0]
    ) / 60

    if total_time == 0:
        return 0

    kpm = total_keys / total_time

    return round(kpm, 2)

def calculate_backspace_ratio(df):
    backspaces = df[df["key"] == "Key.backspace"]

    total_keys = len(df)

    if total_keys == 0:
        return 0

    ratio = len(backspaces) / total_keys

    return round(ratio, 4)

def calculate_interkey_latency(df):
    latencies = []

    press_times = df["press_time"].tolist()

    for i in range(1, len(press_times)):
        latency = press_times[i] - press_times[i - 1]
        latencies.append(latency)

    if len(latencies) == 0:
        return 0

    average_latency = sum(latencies) / len(latencies)

    return round(average_latency, 4)

def main():
    df = load_data()

    typing_speed = calculate_typing_speed(df)
    backspace_ratio = calculate_backspace_ratio(df)
    interkey_latency = calculate_interkey_latency(df)

    print("\n--- FEATURE ANALYSIS ---")

    print(f"Typing Speed: {typing_speed} keys/min")

    print(f"Backspace Ratio: {backspace_ratio}")

    print(f"Average Inter-Key Latency: {interkey_latency} sec")

if __name__ == "__main__":
    main()