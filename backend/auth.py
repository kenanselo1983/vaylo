import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def ensure_users_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        workspace TEXT
    )
    ''')
    conn.commit()
    conn.close()

ensure_users_table()

def authenticate_user(username, password, workspace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=? AND workspace=?", (username, password, workspace))
    result = c.fetchone()
    conn.close()
    if result:
        return True, result[0]
    return False, None

def register_user(username, password, role, workspace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)", (username, password, role, workspace))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, role, workspace FROM users")
    rows = c.fetchall()
    conn.close()
    return rows
