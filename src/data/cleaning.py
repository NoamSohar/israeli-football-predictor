import pandas as pd

def clean_matches(df):
    df = df.copy()

    df = df[df["status"] == "FT"]

    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.sort_values("date")

    return df.reset_index(drop=True)