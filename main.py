"""
Load the raw education-performance and household-income data, produce analysis, and export results.
"""

from pathlib import Path
import pandas as pd

def read_raw_data(file_name: str) -> pd.DataFrame:
    """Read one CSV file from the project's raw-data directory.

    Parameters
    ----------
    file_name : str
        Name of the CSV file in ``data/raw``.

    Returns
    -------
    pandas.DataFrame
        The contents of the requested raw-data file.

    Raises
    ------
    FileNotFoundError
        If the requested source file is missing.
    ValueError
        If the file is not a CSV file.
    """
    file_path = data_path / file_name
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    raise ValueError(f"Unsupported raw-data file type: {file_path.suffix}")

data_path = Path(__file__).resolve().parent / "data" / "raw"
key_stage_4_data = "data-key-stage-4-performance (1).csv"
household_income_data = (
    "regionalgrossdisposablehouseholdincomelocalauthorities2024 (1).csv"
)

key_stage_4_df = read_raw_data(key_stage_4_data)
household_income_df = read_raw_data(household_income_data)