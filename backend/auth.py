import os
import sqlite3

DB_PATH = os.path.abspath("users.db")

def init_user_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                workspace TEXT NOT NULL
            )
        ''')
        c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)",
                  ("admin", "admin", "admin", "default"))
        conn.commit()
        conn.close()

# Ensure DB is initialized on import
init_user_db()

def authenticate_user(username, password, workspace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=? AND workspace=?",
              (username, password, workspace))
    result = c.fetchone()
    conn.close()
    if result:
        return True, result[0]
    return False, None

def register_user(username, password, role, workspace):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)",
                  (username, password, role, workspace))
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
    users = c.fetchall()
    conn.close()
    return users
