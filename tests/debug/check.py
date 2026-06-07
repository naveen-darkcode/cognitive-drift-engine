import sqlite3
import pandas as pd

conn = sqlite3.connect("database/fatigue_logs.db")

print("\nKEYSTROKES")
print(pd.read_sql_query(
    "SELECT DISTINCT session_id FROM keystrokes ORDER BY id DESC LIMIT 5",
    conn
))

print("\nEVENTS")
print(pd.read_sql_query(
    "SELECT DISTINCT user_id FROM events ORDER BY id DESC LIMIT 5",
    conn
))

print("\nLABELS")
print(pd.read_sql_query(
    "SELECT DISTINCT user_id FROM fatigue_labels ORDER BY id DESC LIMIT 5",
    conn
))

conn.close()