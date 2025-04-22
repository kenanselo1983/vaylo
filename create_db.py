import sqlite3

print("Creating database...")

conn = sqlite3.connect("company_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    name TEXT,
    email TEXT,
    created_at TEXT,
    consent_status TEXT,
    legal_basis TEXT
)
""")

sample_data = [
    ("Ali Yılmaz", "ali@example.com", "2021-01-01", "not_given", None),
    ("Ayşe Kaya", "ayse@example.com", "2023-01-01", "given", "contract")
]

cursor.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?)", sample_data)
conn.commit()
conn.close()

print("✅ Done: company_data.db created.")
