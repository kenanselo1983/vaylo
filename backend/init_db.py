# init_db.py
import sqlite3
import os

db_path = os.path.abspath("users.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS users")

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    workspace TEXT NOT NULL
)
""")

c.execute("""
INSERT INTO users (username, password, role, workspace)
VALUES ('admin', 'admin', 'admin', 'default')
""")

conn.commit()
conn.close()

print("✅ users.db reset complete with admin/admin (default)")
