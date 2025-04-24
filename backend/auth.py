import sqlite3
import os

# ✅ Ensure persistent DB location
DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "users.db")

# Create folder if it doesn't exist
os.makedirs(DB_FOLDER, exist_ok=True)

def init_db():
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
    conn.commit()
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

def register_user(username, password, role, workspace):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)", (username, password, role, workspace))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, role, workspace FROM users")
    users = c.fetchall()
    conn.close()
    return users

# ✅ Run once to ensure DB is initialized
init_db()
