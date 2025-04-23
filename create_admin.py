import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("INSERT INTO users (username, password, role, workspace, first_name, last_name, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
          ("admin", "admin", "admin", "default", "Admin", "User", "admin@example.com", "+123456789"))

conn.commit()
conn.close()
print("✅ Admin user created (username: admin, password: admin, workspace: default)")
