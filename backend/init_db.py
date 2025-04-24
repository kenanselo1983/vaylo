# backend/init_db.py
import sqlite3
import os

db_path = os.path.join("data", "users.db")
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(db_path)
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

try:
    c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)",
              ('admin', 'admin', 'admin', 'default'))
    print("✅ Admin user created.")
except sqlite3.IntegrityError:
    print("⚠️ Admin user already exists.")

conn.commit()
conn.close()
