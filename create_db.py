import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()
purposes = ["Internal Audit", "Marketing", "Legal", "Research", "Customer Support"]
data_types = ["Customer Financial Info", "Medical Records", "HR Files", "Payroll", "Usage Logs"]

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

# Add 40 violating rows
violations = [
    ("Marketing", "Medical Records"),
    ("Customer Support", "Payroll"),
    ("Internal Audit", "Medical Records"),
    ("Internal Audit", "Customer Financial Info")
]

for purpose, data_accessed in violations * 10:
    employee_id = f"E{random.randint(1000, 9999)}"
    full_name = faker.name()
    email = faker.email()
    access_time = (datetime.now() - timedelta(days=random.randint(31, 90))).strftime("%Y-%m-%d")  # >30 days
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", 
              (employee_id, full_name, email, data_accessed, access_time, purpose))

# Add 60 clean rows
for _ in range(60):
    employee_id = f"E{random.randint(1000, 9999)}"
    full_name = faker.name()
    email = faker.email()
    purpose = random.choice(purposes)
    data_accessed = random.choice(data_types)
    access_time = (datetime.now() - timedelta(days=random.randint(0, 25))).strftime("%Y-%m-%d")
    c.execute("INSERT INTO company_records VALUES (?, ?, ?, ?, ?, ?)", 
              (employee_id, full_name, email, data_accessed, access_time, purpose))

conn.commit()
conn.close()
print("✅ company_data.db updated with 100 records including violations.")
