import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT,
    workspace TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
''')

conn.commit()
conn.close()
print("✅ users.db created successfully.")
