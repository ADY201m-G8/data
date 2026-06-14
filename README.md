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

## Tests

### 1. Image

Test similality on single image:

```sh
uv run python -m tests.test_similarity
```

The results should look like this:

```
ID                   | Distance   | Cosine Similarity  | Metadata
--------------------------------------------------------------------------------
HE204320             | 0.3404     | 0.6596             | {'fullname': 'Nguyễn Thế Anh'}
HE190781             | 0.6927     | 0.3073             | {'fullname': 'Nguyễn Tuấn Hưng'}
HE201503             | 0.7300     | 0.2700             | {'fullname': 'Cao Biên Thuỳ'}
HE200883             | 0.7693     | 0.2307             | {'fullname': 'Tô Tấn Tài'}
HE161773             | 0.7980     | 0.2020             | {'fullname': 'Nguyễn Đức Long'}
HE171153             | 0.8279     | 0.1721             | {'fullname': 'Đỗ Văn Dũng'}
HE204140             | 0.8312     | 0.1688             | {'fullname': 'Châm Duy Khoát'}
...
```

### 2. Webcam
 
Or, open an OpenCV window:

```sh
uv run python -m tests.test_face_recognition
```
