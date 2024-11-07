# modules/data_exporter.py

import pandas as pd
from config.settings import OUTPUT_PATH

def save_to_excel(data: pd.DataFrame, file_path=OUTPUT_PATH):
    """Save job listings to an Excel file."""
    try:
        data.to_excel(file_path, index=False)
        print(f"Job data saved to {file_path}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")
