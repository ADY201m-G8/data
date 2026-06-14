# Data collection & preperation for ADY201m project

## Preprocessing pipeline

1. Extract CSV from web source
```sh
uv run python -m src.preprocess.1_extract_csv
```

2. Extract images
```sh
uv run python -m src.preprocess.2_extract_img
```

3. Merge CSV
```sh
uv run python -m src.preprocess.3_merge_csv
```

3. Build vector database from images
```sh
uv run python -m src.preprocess.build_vector
```

4. Build SQLite database
```sh
uv run python -m src.preprocess.build_sqlite
```
