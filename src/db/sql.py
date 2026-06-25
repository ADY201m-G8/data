from src import SQLITE_PATH
import os
import sqlite3
from dbml_sqlite import toSQLite


def main():
    ddl = toSQLite('./db/schema.dbml')

    if os.path.exists(SQLITE_PATH):
        os.remove(SQLITE_PATH)

    conn = sqlite3.connect(SQLITE_PATH)
    with conn:
        conn.executescript(ddl)
    conn.close()


if __name__ == "__main__":
    main()
