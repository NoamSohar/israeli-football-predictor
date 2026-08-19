from pathlib import Path
import pandas as pd

def delete_processed_data():
    """
    mainly for debugging and testing purposes
    """
    project_root = Path(__file__).resolve().parents[2]
    processed_data_path = project_root / "data" / "processed" / "processed_data.csv"

    if processed_data_path.exists():
        processed_data_path.unlink()

def get_start_of_season(match_date: pd.Timestamp, matches: pd.DataFrame) -> pd.Timestamp:
    previous_matches = matches[matches["date"] <= match_date]

    round1_matches = previous_matches[previous_matches["round"] == "Regular Season - 1"]
    season_year = round1_matches.iloc[-1]["date"].year

    round1_matches_seasonal = round1_matches[round1_matches["date"].dt.year == season_year]

    return round1_matches_seasonal.iloc[0]["date"]


