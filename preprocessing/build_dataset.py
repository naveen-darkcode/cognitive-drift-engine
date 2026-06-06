import sqlite3
import pandas as pd

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


def calculate_mouse_activity(
    session_events
):

    mouse_events = session_events[
        session_events["event_type"]
        == "mouse_move"
    ]

    return len(mouse_events)


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

                "mouse_activity":
                calculate_mouse_activity(
                    session_events
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