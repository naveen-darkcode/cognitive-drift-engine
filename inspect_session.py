# inspect_session.py

import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/fatigue_logs.db"
)

session_id = "4b708a3f"

events = pd.read_sql_query(
    f"""
    SELECT event_type,
           COUNT(*) as count
    FROM events
    WHERE user_id='{session_id}'
    GROUP BY event_type
    """,
    conn
)

print(events)

conn.close()