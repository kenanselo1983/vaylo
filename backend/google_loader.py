import pandas as pd

def load_google_sheet(url):
    try:
        df = pd.read_csv(url)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Google Sheet load error: {e}")
        return []
