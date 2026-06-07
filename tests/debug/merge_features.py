import sqlite3
import pandas as pd


MY_DB = "database/fatigue_logs.db"
FRIEND_DB = "database/friend_fatigue_logs.db"


def load_features(db_path):

    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query(
        "SELECT * FROM features",
        conn
    )

    conn.close()

    return df


my_features = load_features(MY_DB)

friend_features = load_features(FRIEND_DB)

combined = pd.concat(
    [
        my_features,
        friend_features
    ],
    ignore_index=True
)

combined.to_csv(
    "combined_features.csv",
    index=False
)

print(
    f"My rows: {len(my_features)}"
)

print(
    f"Friend rows: {len(friend_features)}"
)

print(
    f"Combined rows: {len(combined)}"
)

print(
    "\nSaved: combined_features.csv"
)