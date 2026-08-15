from data.load import load_all_seasons
from data.validation import validate_matches
from data.cleaning import clean_matches
import pandas as pd

def process_matches() -> pd.DataFrame:
    df = load_all_seasons()

    validate_matches(df)

    df = clean_matches(df)

    validate_matches(df)

    return df