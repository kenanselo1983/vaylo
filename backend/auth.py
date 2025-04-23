import sqlite3

def authenticate_user(username, password, workspace):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=? AND workspace=?", (username, password, workspace))
    result = c.fetchone()
    conn.close()
    if result:
        return True, result[0]
    return False, None

def register_user(username, password, role, workspace, first_name, last_name, email, phone):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False  # User already exists
    c.execute('''
        INSERT INTO users (username, password, role, workspace, first_name, last_name, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, role, workspace, first_name, last_name, email, phone))
    conn.commit()
    conn.close()
    return True

def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, role, workspace, first_name, last_name, email, phone FROM users")
    users = c.fetchall()
    conn.close()
    return users
