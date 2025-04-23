import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Create users table with workspace column
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    workspace TEXT
)
""")

# Optional: insert default admin
try:
    c.execute("INSERT INTO users (username, password, role, workspace) VALUES (?, ?, ?, ?)", ("admin", "admin", "admin", "default"))
except:
    pass

conn.commit()
conn.close()

print("✅ users.db fixed with workspace support")
