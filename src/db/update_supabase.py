import csv
import os
from itertools import chain
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

from src import PROCESSED_DATA_PATH
from src.db.utils import csv_to_dict

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", default="")
key: str = os.environ.get("SUPABASE_KEY", default="")

supabase: Client = create_client(url, key)


def parse_enrollments_csv(csv_path: Path) -> list[dict]:
    subject_id = csv_path.stem
    with csv_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        data = [
            {"student_id": row[0], "subject_id": subject_id} for row in reader if row
        ]

        return data


def main():
    csv_paths = list((PROCESSED_DATA_PATH / "subjects").glob("*.csv"))

    students = csv_to_dict(PROCESSED_DATA_PATH / "students.csv")
    subjects = list(map(lambda p: {"id": p.stem}, csv_paths))
    enrollments = list(chain.from_iterable(map(parse_enrollments_csv, csv_paths)))

    supabase.table("students").upsert(students).execute()
    supabase.table("subjects").upsert(subjects).execute()
    supabase.table("enrollments").upsert(enrollments).execute()


if __name__ == "__main__":
    main()
