import csv
from pathlib import Path


def csv_to_dict(csv_path: Path) -> list[dict]:
    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data_list = list(reader)

        return data_list
