import sqlite3
import pandas as pd

from database.db import insert_feature_row

DB_NAME = "database/fatigue_logs.db"

WINDOW_SIZE = 10


def load_keystrokes():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM keystrokes",
        conn
    )

    conn.close()

    return df


def load_events():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM events",
        conn
    )

    conn.close()

    return df


def load_labels():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM fatigue_labels",
        conn
    )

    conn.close()

    return df


def clear_features_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM features"
    )

    conn.commit()

    conn.close()


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

    press_times = window[
        "press_time"
    ].tolist()

    latencies = []

    for i in range(
        1,
        len(press_times)
    ):

        latencies.append(
            press_times[i]
            - press_times[i - 1]
        )

    if len(latencies) < 2:
        return 0

    return round(
        pd.Series(latencies).var(),
        4
    )


def calculate_typing_speed(window):

    total_keys = len(window)

    if total_keys < 2:
        return 0

    duration = (
        window["release_time"].max()
        - window["press_time"].min()
    )

    if duration <= 0:
        return 0

    typing_speed = (
        total_keys / duration
    ) * 60

    return round(
        typing_speed,
        2
    )


def calculate_mouse_activity(
    session_events,
    start_time,
    end_time
):

    count = 0

    mouse_events = session_events[
        session_events["event_type"]
        == "mouse_move"
    ]

    for _, row in mouse_events.iterrows():

        try:

            event_ts = float(
                row["ts"]
            )

            if (
                start_time
                <= event_ts
                <= end_time
            ):
                count += 1

        except Exception:
            pass

    return count


def calculate_click_count(
    session_events,
    start_time,
    end_time
):

    count = 0

    click_events = session_events[
        session_events["event_type"]
        == "mouse_click"
    ]

    for _, row in click_events.iterrows():

        try:

            event_ts = float(
                row["ts"]
            )

            if (
                start_time
                <= event_ts
                <= end_time
            ):
                count += 1

        except Exception:
            pass

    return count


def calculate_app_switch_rate(
    session_events
):

    focus_events = session_events[
        session_events["event_type"]
        == "focus_change"
    ]

    return len(focus_events)


def get_session_label(
    labels_df,
    session_id
):

    session_labels = labels_df[
        labels_df["user_id"]
        == session_id
    ]

    if session_labels.empty:
        return None

    return int(
        session_labels.iloc[-1]["label"]
    )


def build_dataset():

    keystrokes_df = load_keystrokes()

    events_df = load_events()

    labels_df = load_labels()

    clear_features_table()

    dataset_rows = []

    sessions = (
        keystrokes_df["session_id"]
        .unique()
    )

    for session_id in sessions:

        session_df = keystrokes_df[
            keystrokes_df["session_id"]
            == session_id
        ]

        session_events = events_df[
            events_df["user_id"]
            == session_id
        ]

        fatigue_label = get_session_label(
            labels_df,
            session_id
        )

        print(
            f"Session={session_id} | "
            f"Rows={len(session_df)} | "
            f"Events={len(session_events)} | "
            f"Label={fatigue_label}"
        )

        if fatigue_label is None:
            continue

        for start in range(
            0,
            len(session_df),
            WINDOW_SIZE
        ):

            end = start + WINDOW_SIZE

            window = session_df.iloc[
                start:end
            ]

            if len(window) < WINDOW_SIZE:
                continue

            window_start = (
                window["press_time"].min()
            )

            window_end = (
                window["release_time"].max()
            )

            row = {

                "session_id":
                session_id,

                "iki_variance":
                calculate_iki_variance(
                    window
                ),

                "backspace_ratio":
                calculate_backspace_ratio(
                    window
                ),

                "dwell_time":
                calculate_average_dwell_time(
                    window
                ),

                "typing_speed":
                calculate_typing_speed(
                    window
                ),

                "mouse_activity":
                calculate_mouse_activity(
                    session_events,
                    window_start,
                    window_end
                ),

                "click_count":
                calculate_click_count(
                    session_events,
                    window_start,
                    window_end
                ),

                "app_switch_rate":
                calculate_app_switch_rate(
                    session_events
                ),

                "fatigue_label":
                fatigue_label
            }

            dataset_rows.append(
                row
            )

            insert_feature_row(
                session_id,
                row["iki_variance"],
                row["backspace_ratio"],
                row["dwell_time"],
                row["typing_speed"],
                row["mouse_activity"],
                row["click_count"],
                row["app_switch_rate"],
                row["fatigue_label"]
            )

    dataset = pd.DataFrame(
        dataset_rows
    )

    dataset.to_csv(
        "features.csv",
        index=False
    )

    print(
        f"\nDataset saved with "
        f"{len(dataset)} rows\n"
    )

    print(dataset)


if __name__ == "__main__":

    build_dataset()