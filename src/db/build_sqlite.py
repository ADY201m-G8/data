from src import SQLITE_PATH
import os
import sqlite3
from dbml_sqlite import toSQLite

import csv
import os
import sqlite3
from pathlib import Path

from src import SQLITE_PATH, PROCESSED_DATA_PATH


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


def parse_enrollments_csv(csv_path: Path) -> list[tuple]:
    subject_id = csv_path.stem
    with csv_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        data = [(row[0], subject_id) for row in reader if row]
        return data


def write_sqlite(db_path: Path, students: list[tuple], subjects: list[tuple], enrollments: list[tuple]) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT INTO students (id, name)
            VALUES (?, ?)
            """,
            students,
        )

        cursor.executemany(
            """
            INSERT INTO subjects (id)
            VALUES (?)
            """,
            subjects,
        )

        cursor.executemany(
            """
            INSERT INTO enrollments (student_id, subject_id)
            VALUES (?, ?)
            """,
            enrollments,
        )

        cursor.executemany(
            """
            INSERT INTO rooms (id)
            VALUES (?)
            """,
            [("B102",), ("B315",)],
        )

        conn.commit()


def main():
    dbml2sqlite(Path("./db/schema.dbml"), SQLITE_PATH)

    csv_paths = list((PROCESSED_DATA_PATH / "subjects").glob("*.csv"))

    students = parse_students_csv(PROCESSED_DATA_PATH / "students.csv")
    subjects = list(map(lambda p: (p.stem, ), csv_paths))
    enrollments = []
    for csv_path in csv_paths:
        enrollments.extend(parse_enrollments_csv(csv_path))

    write_sqlite(SQLITE_PATH, students, subjects, enrollments)


if __name__ == "__main__":
    main()
