import sqlite3
from datetime import datetime

DB_NAME = "weather.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature_c REAL NOT NULL,
            temperature_f REAL NOT NULL,
            humidity REAL NOT NULL,
            rssi INTEGER,
            vcc REAL,
            uptime INTEGER,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_reading(temp_c, temp_f, humidity, rssi=None, vcc=None, uptime=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO readings 
        (temperature_c, temperature_f, humidity, rssi, vcc, uptime, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (temp_c, temp_f, humidity, rssi, vcc, uptime, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_readings():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM readings ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_latest_reading():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row