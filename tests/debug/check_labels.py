import sqlite3

conn = sqlite3.connect(
    "database/fatigue_logs.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM fatigue_labels"
)

for row in cursor.fetchall():
    print(row)

conn.close()