import sqlite3
from datetime import datetime
import os

DB_FILE = './database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            original_name TEXT,
            version INTEGER,
            upload_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_file(filename, original_name, version):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO files (filename, original_name, version, upload_time)
        VALUES (?, ?, ?, ?)
    ''', (filename, original_name, version, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_files():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT original_name, filename, version, upload_time
        FROM files
        ORDER BY original_name, version
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_file_versions(original_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT filename, version
        FROM files
        WHERE original_name = ?
        ORDER BY version
    ''', (original_name,))
    rows = c.fetchall()
    conn.close()
    return rows
