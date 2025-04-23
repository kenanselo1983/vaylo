import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'users.db')

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

def authenticate_user(username, password, workspace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=? AND workspace=?", (username, password, workspace))
    result = c.fetchone()
    conn.close()
    if result:
        return True, result[0]
    return False, None

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, role, workspace FROM users")
    users = c.fetchall()
    conn.close()
    return users
