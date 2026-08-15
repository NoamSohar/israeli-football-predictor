import pandas as pd

def clean_matches(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df[df["status"] == "FT"]
    df = df.sort_values("date")
    df = df.reset_index(drop=True)

    return df