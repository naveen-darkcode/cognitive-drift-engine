import sqlite3

conn = sqlite3.connect(
    "database/fatigue_logs.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT session_id
FROM keystrokes
""")

for row in cursor.fetchall():
    print(row[0])

conn.close()