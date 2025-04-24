# ✅ backend/google_loader.py

import pandas as pd

def load_google_sheet(url: str) -> pd.DataFrame:
    """
    Loads a Google Sheet in CSV format and returns a DataFrame.
    The URL must end with: /gviz/tq?tqx=out:csv

    Args:
        url (str): Google Sheet CSV URL

    Returns:
        pd.DataFrame: Parsed data as DataFrame
    """
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load Google Sheet: {e}")
