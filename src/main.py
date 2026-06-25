from src.preprocess import pipeline
from src.db import (
    build_sqlite,
    build_chromadb
)

def main():
    pipeline.main()

    build_sqlite.main()
    build_chromadb.main()


if __name__ == "__main__":
    main()
