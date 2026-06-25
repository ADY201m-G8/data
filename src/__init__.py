import os
from pathlib import Path

DB_PATH = Path("./db")
DB_PATH.mkdir(exist_ok=True)
RAW_DATA_PATH = Path("./data/raw/")
RAW_DATA_PATH.mkdir(exist_ok=True)
PROCESSED_DATA_PATH = Path("./data/processed/")
PROCESSED_DATA_PATH.mkdir(exist_ok=True)

WEB_SOURCE_PATH = RAW_DATA_PATH / "web"
WEB_SOURCE_PATH.mkdir(exist_ok=True)
RAW_CSV_PATH = RAW_DATA_PATH / "csv"
RAW_CSV_PATH.mkdir(exist_ok=True)
RAW_IMG_FOLDER_PATH = RAW_DATA_PATH / "imgs"
RAW_IMG_FOLDER_PATH.mkdir(exist_ok=True)

CROPPED_IMG_FOLDER_PATH = PROCESSED_DATA_PATH / "imgs"
CROPPED_IMG_FOLDER_PATH.mkdir(exist_ok=True)

SQLITE_PATH = DB_PATH / "db.sqlite3"
CHROMA_DB_FOLDER_PATH = DB_PATH / "chroma"

EMBEDDING_MODEL = "buffalo_sc"
EXECUTION_PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]
