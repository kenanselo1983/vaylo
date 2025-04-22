import sqlite3

def fetch_data_from_db(db_path="company_data.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()

    data = [dict(row) for row in rows]
    conn.close()
    return data
