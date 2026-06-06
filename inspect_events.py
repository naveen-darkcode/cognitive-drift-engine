# inspect_events.py

import sqlite3
import pandas as pd

conn = sqlite3.connect("database/fatigue_logs.db")

df = pd.read_sql_query(
    "SELECT ts,event_type FROM events LIMIT 5",
    conn
)

print(df)

conn.close()