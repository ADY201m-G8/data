from functools import reduce
from pathlib import Path

import pandas as pd

from src.preprocess import RAW_CSV_PATH, PROCESSED_DATA_PATH


def process_csv(csv_path: Path) -> pd.DataFrame:
    return (
        pd.read_csv(csv_path)
        .drop(columns=["Index", "Image"], errors="ignore")
        .assign(
            Fullname=lambda df: (
                df["Surname"].fillna("")
                + " "
                + df["Middle name"].fillna("")
                + " "
                + df["Given name"].fillna("")
            )
        )
        .assign(
            Fullname=lambda df: (
                df["Fullname"].str.strip().str.replace(r"\s+", " ", regex=True)
            )
        )
        .drop(columns=["Surname", "Middle name", "Given name"], errors="ignore")
    )


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2], ignore_index=True).drop_duplicates(
        subset=["Code"], keep="first"
    )


def process_and_merge_csvs(file_paths: list[Path]) -> pd.DataFrame:
    return (
        reduce(merge_dataframes, map(process_csv, file_paths))
        if file_paths
        else pd.DataFrame()
    )


if __name__ == "__main__":
    csv_list = list(RAW_CSV_PATH.glob("*.csv"))
    final_df = process_and_merge_csvs(csv_list)
    final_df.to_csv(PROCESSED_DATA_PATH / "students.csv", index=False)
