import os
from pathlib import Path

DB_PATH = Path("./db")
RAW_DATA_PATH = Path("./data/raw/")
PROCESSED_DATA_PATH = Path("./data/processed/")

WEB_SOURCE_PATH = RAW_DATA_PATH / "web"
RAW_CSV_PATH = RAW_DATA_PATH / "csv"
RAW_IMG_FOLDER_PATH = RAW_DATA_PATH / "imgs"

CROPPED_IMG_FOLDER_PATH = PROCESSED_DATA_PATH / "imgs"

SQLITE_PATH = DB_PATH / "db.sqlite3"
CHROMA_DB_FOLDER_PATH = DB_PATH / "chroma"

EMBEDDING_MODEL = "buffalo_sc"
EXECUTION_PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]


os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
