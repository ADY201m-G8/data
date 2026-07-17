# 📦 **Data collection & preperation for ADY201m project**

## 🔧 **Project setup**

First, install [uv](https://docs.astral.sh/uv/getting-started/installation/)

Then, setup virtual env:

```sh
uv sync
```

## 🚈 **Pipeline**

```sh
uv run python -m src.main
```

This single `main.py` run:

- Data processing pipeline
- Generate ChromaDB
- Generate SQLite db
- Update Supabase db

Just that.

## 🖼️ **Results**

### **Images & CSVs**

```sh
/data
├── /processed
│   ├── /imgs               # Square cropped face images
│   ├── /subjects           # CSV files of subjects (student id, student name)
│   └── students.csv        # All students (id, name)
└── /raw                    # Raw data
    ├── /csv                # Raw csv extracted for tables in web source
    ├── /imgs               # Extracted images from web source
    └── /web                # Raw crawled web source
```

### **DBs**

```sh
/db
├── /chroma                 # ChromaDB (saved by `chromadb.PersistentClient`)
└── db.sqlite3              # Generated SQLite db for backup
```

And sync with **Supabase** db if `SUPABASE_URL` and `SUPABASE_KEY` provided in `.env`.

## 📦 **Processed data**

You can download processed data in 👉 [Releases](https://github.com/ADY201m-G8/data/releases) page.
