import sqlite3

DB_NAME = "database/fatigue_logs.db"

def create_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keystrokes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    key TEXT,
    press_time REAL,
    release_time REAL,
    dwell_time REAL
 )
  """)

    conn.commit()
    conn.close()

def insert_keystroke(
    session_id,key,press_time,release_time,dwell_time):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO keystrokes (
    session_id,
    key,
    press_time,
    release_time,
    dwell_time
)
VALUES (?, ?, ?, ?, ?)
    """, (
    session_id,
    key,
    press_time,
    release_time,
    dwell_time
))

    conn.commit()
    conn.close()