import sqlite3
import json
from datetime import datetime

DB_NAME = "database/fatigue_logs.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Existing table (keep for compatibility)
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

    # New unified events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        ts TEXT,
        event_type TEXT,
        payload TEXT
    )
    """)

    # Fatigue labels table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fatigue_labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        ts TEXT,
        label INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_keystroke(
    session_id,
    key,
    press_time,
    release_time,
    dwell_time
):
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


def insert_event(
    user_id,
    event_type,
    payload
):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events (
        user_id,
        ts,
        event_type,
        payload
    )
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        datetime.now().isoformat(),
        event_type,
        json.dumps(payload)
    ))

    conn.commit()
    conn.close()


def insert_fatigue_label(
    user_id,
    label
):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fatigue_labels (
        user_id,
        ts,
        label
    )
    VALUES (?, ?, ?)
    """, (
        user_id,
        datetime.now().isoformat(),
        label
    ))

    conn.commit()
    conn.close()