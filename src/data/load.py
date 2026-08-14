from pathlib import Path
import pandas as pd

raw_data_dir = Path("data/raw")

def load_season(file_name: str) -> pd.DataFrame:
    path = raw_data_dir / file_name

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)

def load_all_seasons(file_name: str) -> pd.DataFrame:

    file_names = raw_data_dir.glob("*.csv")

    if not file_names:
        raise FileNotFoundError("No match files found in data/raw")

    data_frames = []
    for file in file_names:
        data_frames.append(pd.read_csv(file))

    return pd.concat(data_frames, ignore_index=True)

