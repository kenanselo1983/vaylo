import sqlite3
import pandas as pd

def fetch_data_from_db():
    conn = sqlite3.connect("company_data.db")
    df = pd.read_sql_query("SELECT * FROM company_records", conn)
    conn.close()
    return df.to_dict(orient="records")
