import pandas as pd

# Default public Google Sheet URL (you can override from app.py)
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/10DReLchE2zNPvbqEIf19XU69lpni_0-w1NTOBFnhN34/gviz/tq?tqx=out:csv"

def load_google_sheet(sheet_url=DEFAULT_SHEET_URL):
    try:
        df = pd.read_csv(sheet_url)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Failed to load Google Sheet: {e}")
        return []
