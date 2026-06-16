import os
from functools import reduce
from pathlib import Path

import pandas as pd

from src import PROCESSED_DATA_PATH, RAW_CSV_PATH


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


def process_and_merge_csvs(csv_paths: list[Path]) -> pd.DataFrame:
    return (
        reduce(merge_dataframes, map(process_csv, csv_paths))
        if csv_paths
        else pd.DataFrame()
    )


def main() -> None:
    csv_list = list(RAW_CSV_PATH.glob("*.csv"))

    df = process_and_merge_csvs(csv_list)

    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH / "students.csv", index=False)


if __name__ == "__main__":
    main()
