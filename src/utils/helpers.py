from pathlib import Path
import os

def delete_processed_data():
    """
    mainly for debugging and testing purposes
    """
    project_root = Path(__file__).resolve().parents[2]
    processed_data_dir = project_root / "data" / "processed" / "processed_data.csv"

    os.remove(processed_data_dir)