import csv
import os
import sqlite3
from pathlib import Path

from src import DB_FOLDER_PATH, PROCESSED_DATA_PATH


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
        )
        """
    )


def insert_students(cursor: sqlite3.Cursor, data: list[tuple]) -> None:
    cursor.executemany(
        """
        INSERT OR REPLACE INTO student (id, fullname)
        VALUES (?, ?)
        """,
        data,
    )


def save_to_sqlite(db_path: Path, data: list[tuple[str, str]]) -> None:
    os.makedirs(DB_FOLDER_PATH, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        init_db(cursor)
        insert_students(cursor, data)
        conn.commit()


def main():
    data = process_csv(PROCESSED_DATA_PATH / "students.csv")
    save_to_sqlite(DB_FOLDER_PATH / "db.sqlite3", data)


if __name__ == "__main__":
    main()
