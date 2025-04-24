import sqlite3
import os

DB_PATH = os.path.join("backend", "users.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    workspace TEXT NOT NULL
)
""")

try:
    c.execute("INSERT INTO users (username, password, role, workspace) VALUES ('admin', 'admin', 'admin', 'default')")
except sqlite3.IntegrityError:
    print("✅ Admin user already exists")

conn.commit()
conn.close()
print("✅ Database initialized at backend/users.db")
