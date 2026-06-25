import csv
from pathlib import Path

import chromadb
import cv2
import numpy as np
from insightface.app import FaceAnalysis

from src import (
    SQLITE_PATH,
    EMBEDDING_MODEL,
    PROCESSED_DATA_PATH,
    RAW_IMG_FOLDER_PATH,
)

app = FaceAnalysis(name=EMBEDDING_MODEL, providers=["CUDAExecutionProvider"])
app.prepare(ctx_id=0, det_size=(224, 224))


def parse_csv_to_dict(csv_path: Path) -> dict[str, str]:
    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {row["Code"]: row["Fullname"] for row in reader}


def extract_embedding(img_path: Path) -> np.ndarray:
    img = cv2.imread(str(img_path))

    if img is None:
        return np.zeros(512)

    faces = app.get(img)

    if not faces:
        print(f"Warning: no face found in {img_path}")
        return np.zeros(512)

    return faces[0].normed_embedding


def save_to_chroma(
    ids: list[str],
    embeddings: list[np.ndarray],
    fullnames: list[str],
) -> None:
    client = chromadb.PersistentClient(path=SQLITE_PATH / "chroma")
    collection = client.get_or_create_collection(
        name="all", metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=[{"fullname": fullname} for fullname in fullnames],
    )


def main() -> None:
    img_paths = list(RAW_IMG_FOLDER_PATH.glob("*"))
    fullnames_dict = parse_csv_to_dict(PROCESSED_DATA_PATH / "students.csv")

    keys = []
    fullnames = []
    embeddings = []

    for img_path in img_paths:
        student_code = img_path.stem
        embedding = extract_embedding(img_path)

        keys.append(student_code)
        fullnames.append(fullnames_dict[student_code])
        embeddings.append(embedding)

    save_to_chroma(keys, embeddings, fullnames)


if __name__ == "__main__":
    main()
