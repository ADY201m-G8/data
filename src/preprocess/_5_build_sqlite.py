import csv
import os
import sqlite3
from pathlib import Path

from src import DB_FOLDER_PATH, PROCESSED_DATA_PATH

SUBJECTS = ["ADY201m", "JPD123", "MAI391", "MAS291"]

def process_csv(path: Path) -> list[tuple]:
    with path.open(mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        data = [tuple(row) for row in reader if row]
        return data


def init_db(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student (
            [id] TEXT PRIMARY KEY,
            [fullname] TEXT NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subject (
            [id] TEXT PRIMARY KEY
        );
        """
    )
            


def insert_rows(cursor: sqlite3.Cursor, students: list[tuple], subjects: list[str]) -> None:
    cursor.executemany(
        """
        INSERT INTO student (id, fullname)
        VALUES (?, ?)
        """,
        students,
    )
    formatted_subjects = [(subject,) for subject in subjects]
    cursor.executemany(
        """
        INSERT INTO subject (id)
        VALUES (?)
        """,
        formatted_subjects,
    )


def save_to_sqlite(db_path: Path, students: list[tuple], subjects: list[str]) -> None:
    os.makedirs(DB_FOLDER_PATH, exist_ok=True)
    os.remove(db_path) if db_path.exists() else None

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        init_db(cursor)
        insert_rows(cursor, students, subjects)
        conn.commit()


def main():
    data = process_csv(PROCESSED_DATA_PATH / "students.csv")
    save_to_sqlite(DB_FOLDER_PATH / "db.sqlite3", data, SUBJECTS)


if __name__ == "__main__":
    main()
