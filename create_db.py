import sqlite3
from faker import Faker
from datetime import datetime, timedelta
import random

faker = Faker()
conn = sqlite3.connect("company_data.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS company_records")
c.execute("""
CREATE TABLE company_records (
    employee_id TEXT,
    full_name TEXT,
    email TEXT,
    data_accessed TEXT,
    access_time TEXT,
    purpose TEXT
)
""")

# Violation 1: Marketing accessing Medical Records
for _ in range(10):
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", (
        f"E{random.randint(1000,9999)}",
        faker.name(),
        faker.email(),
        "Medical Records",
        datetime.now().strftime("%Y-%m-%d"),
        "Marketing"
    ))

# Violation 2: Customer Support accessing Payroll
for _ in range(10):
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", (
        f"E{random.randint(1000,9999)}",
        faker.name(),
        faker.email(),
        "Payroll",
        datetime.now().strftime("%Y-%m-%d"),
        "Customer Support"
    ))

# Violation 3: Internal Audit accessing unauthorized data
for _ in range(10):
    invalid_data = random.choice(["Medical Records", "Customer Financial Info", "Payroll"])
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", (
        f"E{random.randint(1000,9999)}",
        faker.name(),
        faker.email(),
        invalid_data,
        datetime.now().strftime("%Y-%m-%d"),
        "Internal Audit"
    ))

# Violation 4: Data older than 30 days
for _ in range(10):
    old_date = (datetime.now() - timedelta(days=random.randint(31, 90))).strftime("%Y-%m-%d")
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", (
        f"E{random.randint(1000,9999)}",
        faker.name(),
        faker.email(),
        "HR Files",
        old_date,
        "Legal"
    ))

# Clean data rows
clean_data_types = ["HR Files", "Usage Logs"]
clean_purposes = ["Legal", "Research"]
for _ in range(40):
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", (
        f"E{random.randint(1000,9999)}",
        faker.name(),
        faker.email(),
        random.choice(clean_data_types),
        datetime.now().strftime("%Y-%m-%d"),
        random.choice(clean_purposes)
    ))

conn.commit()
conn.close()
print("✅ Database generated with 100 rows (40 with known violations).")
