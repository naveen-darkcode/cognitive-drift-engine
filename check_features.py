import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/fatigue_logs.db"
)

df = pd.read_sql_query(
    "SELECT * FROM features",
    conn
)

print(df)

conn.close()