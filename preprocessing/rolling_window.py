import sqlite3
import pandas as pd

DB_NAME = "database/fatigue_logs.db"

WINDOW_SIZE = 20


def load_session_data(session_id):

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM keystrokes
    WHERE session_id = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(session_id,)
    )

    conn.close()

    return df


def calculate_backspace_ratio(window):

    total_keys = len(window)

    if total_keys == 0:
        return 0

    backspaces = window[
        window["key"] == "Key.backspace"
    ]

    return round(
        len(backspaces) / total_keys,
        4
    )


def calculate_average_dwell_time(window):

    if len(window) == 0:
        return 0

    return round(
        window["dwell_time"].mean(),
        4
    )


def calculate_iki_variance(window):

    press_times = window["press_time"].tolist()

    latencies = []

    for i in range(1, len(press_times)):

        latency = (
            press_times[i]
            - press_times[i - 1]
        )

        latencies.append(latency)

    if len(latencies) < 2:
        return 0

    return round(
        pd.Series(latencies).var(),
        4
    )


def analyze_windows(df):

    print(
        "\n===== Rolling Window Analysis =====\n"
    )

    for start in range(
        0,
        len(df),
        WINDOW_SIZE
    ):

        end = start + WINDOW_SIZE

        window = df.iloc[start:end]

        if len(window) < WINDOW_SIZE:
            continue

        print(
            f"\nWindow {start // WINDOW_SIZE + 1}"
        )

        print(
            "Backspace Ratio:",
            calculate_backspace_ratio(window)
        )

        print(
            "Average Dwell Time:",
            calculate_average_dwell_time(window)
        )

        print(
            "IKI Variance:",
            calculate_iki_variance(window)
        )

        print("-" * 40)


def main():

    session_id = input(
        "Enter Session ID: "
    )

    df = load_session_data(session_id)

    if df.empty:

        print("No data found.")

        return

    analyze_windows(df)


if __name__ == "__main__":
    main()