import sqlite3
import pandas as pd

DB_NAME = "database/fatigue_logs.db"


def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM keystrokes
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def calculate_backspace_ratio(df):

    total_keys = len(df)

    if total_keys == 0:
        return 0

    backspaces = df[
        df["key"] == "Key.backspace"
    ]

    return round(
        len(backspaces) / total_keys,
        4
    )


def calculate_average_dwell_time(df):

    if len(df) == 0:
        return 0

    return round(
        df["dwell_time"].mean(),
        4
    )


def calculate_iki_variance(df):

    press_times = df["press_time"].tolist()

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


def main():

    df = load_data()

    print("\n===== FEATURE ANALYSIS =====\n")

    print(
        "Backspace Ratio:",
        calculate_backspace_ratio(df)
    )

    print(
        "Average Dwell Time:",
        calculate_average_dwell_time(df)
    )

    print(
        "IKI Variance:",
        calculate_iki_variance(df)
    )


if __name__ == "__main__":
    main()