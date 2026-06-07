# inspect_latest_events.py

import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/fatigue_logs.db"
)

df = pd.read_sql_query(
    """
    SELECT id, user_id, ts, event_type
    FROM events
    ORDER BY id DESC
    LIMIT 20
    """,
    conn
)

print(df)

conn.close()