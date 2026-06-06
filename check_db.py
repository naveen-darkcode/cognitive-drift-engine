import sqlite3

conn = sqlite3.connect("database/fatigue_logs.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM keystrokes")
print("Keystrokes:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM events")
print("Events:", cursor.fetchone()[0])

conn.close()