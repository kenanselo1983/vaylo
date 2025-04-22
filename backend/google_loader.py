import pandas as pd

def load_google_sheet(sheet_url):
    try:
        df = pd.read_csv(sheet_url)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Google Sheet Load Failed: {e}")
        return []
