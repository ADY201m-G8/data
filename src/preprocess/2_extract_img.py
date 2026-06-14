import csv
import os
import shutil
from pathlib import Path

from src.preprocess import CSV_PATH, IMAGE_PATH, WEB_SOURCE_PATH


def process_on_csv(csv_path: Path) -> None:
    success_count = 0

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            relative_image_path = row["Image"]
            student_code = row["Code"]

            suffix = Path(relative_image_path).suffix

            if suffix not in [".jpg", ".jpeg", ".png"]:
                continue

            source_path = os.path.join(WEB_SOURCE_PATH, relative_image_path)

            destination_path = IMAGE_PATH / f"{student_code}{suffix}"

            if os.path.exists(source_path):
                os.makedirs(IMAGE_PATH, exist_ok=True)
                shutil.copy2(source_path, destination_path)
                success_count += 1
            else:
                print(f"Image not found: {source_path}")

    print(f"Extracted {success_count} images from {csv_path}")


def process_on_csv_dataset() -> None:
    csvs = list(CSV_PATH.glob("*.csv"))

    for csv_file in csvs:
        process_on_csv(csv_file)


if __name__ == "__main__":
    process_on_csv_dataset()
