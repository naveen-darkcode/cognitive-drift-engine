import sqlite3

conn = sqlite3.connect("database/fatigue_logs.db")
cursor = conn.cursor()

cursor.execute("""
SELECT event_type, COUNT(*)
FROM events
GROUP BY event_type
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()