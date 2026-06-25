from src import SQLITE_PATH
import os
import sqlite3
from dbml_sqlite import toSQLite

import csv
import os
import sqlite3
from pathlib import Path

from src import SQLITE_PATH, PROCESSED_DATA_PATH

SUBJECTS = ["ADY201m", "JPD123", "MAI391", "MAS291"]


def dbml2sqlite(dbml_path: Path, sqlite_path: Path):
    ddl = toSQLite(str(dbml_path))

    os.remove(sqlite_path) if sqlite_path.exists() else None

    conn = sqlite3.connect(sqlite_path)
    with conn:
        conn.executescript(ddl)
    conn.close()


def parse_students_csv(csv_path: Path) -> list[tuple]:
    with csv_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        data = [tuple(row) for row in reader if row]
        return data


def write_sqlite(db_path: Path, students: list[tuple], subjects: list[str]) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT INTO students (id, name)
            VALUES (?, ?)
            """,
            students,
        )

        formatted_subjects = [(subject,) for subject in subjects]
        cursor.executemany(
            """
            INSERT INTO subjects (code)
            VALUES (?)
            """,
            formatted_subjects,
        )

        conn.commit()


def main():
    dbml2sqlite(Path("./db/schema.dbml"), SQLITE_PATH)

    students = parse_students_csv(PROCESSED_DATA_PATH / "students.csv")

    write_sqlite(SQLITE_PATH, students, SUBJECTS)


if __name__ == "__main__":
    main()
