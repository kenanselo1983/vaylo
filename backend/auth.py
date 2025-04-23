import sqlite3

def connect_db():
    return sqlite3.connect("users.db")

def register_user(username, password, role, workspace):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                workspace TEXT NOT NULL
            )
        ''')
        c.execute('INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)',
                  (username, password, role, workspace))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT username, role, workspace FROM users")
    rows = c.fetchall()
    conn.close()
    return [{"username": u, "role": r, "workspace": w} for (u, r, w) in rows]
