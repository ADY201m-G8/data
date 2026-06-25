import os
from functools import reduce
from pathlib import Path

import pandas as pd

from src import PROCESSED_DATA_PATH, RAW_CSV_PATH


def process_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df.drop(columns=["Index", "Image"], errors="ignore", inplace=True)
    df = df.assign(Fullname=lambda df: (
            df["Surname"].fillna("")
            + " "
            + df["Middle name"].fillna("")
            + " "
            + df["Given name"].fillna("")
        )
    )
    df = df.assign(Fullname=lambda df: df["Fullname"].str.strip().str.replace(r"\s+", " ", regex=True))
    df.drop(columns=["Surname", "Middle name", "Given name"], errors="ignore", inplace=True)

    df.rename(columns={"Code": "id", "Fullname": "name"}, inplace=True)

    return df


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2], ignore_index=True).drop_duplicates(
        subset=["id"], keep="first"
    )


def main() -> None:
    csv_paths = list(RAW_CSV_PATH.glob("*.csv"))
    subject_dfs = list(map(process_csv, csv_paths))

    os.makedirs(PROCESSED_DATA_PATH / "subjects", exist_ok=True)
    for csv_path, subject_df in zip(csv_paths, subject_dfs):
        subject_df.to_csv(PROCESSED_DATA_PATH / "subjects" / csv_path.name, index=False)

    all_students_df = reduce(merge_dataframes, subject_dfs)
    all_students_df.to_csv(PROCESSED_DATA_PATH / "students.csv", index=False)


if __name__ == "__main__":
    main()
