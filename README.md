# Data collection & preperation for ADY201m project

## Project setup

First, install [uv](https://docs.astral.sh/uv/getting-started/installation/)

Then run in project root:

```sh
uv sync
```

## Preprocessing pipeline

```sh
uv run python -m src.preprocess.pipeline
```

Results stored in *`data/processed/`*.
