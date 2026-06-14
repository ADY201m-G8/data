from pathlib import Path
from typing import Dict, List

import cv2
import numpy as np
from insightface.app import FaceAnalysis

import os
from typing import Any, Dict, Optional
import chromadb
from numpy import ndarray


app = FaceAnalysis(allowed_modules=["detection", "recognition"])
app.prepare(ctx_id=0, det_size=(240, 240))


def get_image_paths(folder_path: Path) -> List[Path]:
    """Pure function to get all image file paths from a directory using pathlib."""
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    return [
        p
        for p in folder_path.iterdir()
        if p.is_file() and p.suffix.lower() in valid_extensions
    ]


def extract_embedding(image_path: Path) -> np.ndarray:
    """Pure function that maps a Path object to its primary ArcFace embedding vector.

    Returns a zero-vector if no face is detected.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return np.zeros(512)

    faces = app.get(img)
    return faces[0].normed_embedding if faces else np.zeros(512)


def process_images(folder_path: Path) -> Dict[str, np.ndarray]:
    """High-level pipeline transforming paths into the final dictionary structure."""
    img_paths = get_image_paths(folder_path)

    dictionary = {}
    for img_path in img_paths:
        student_code = img_path.stem
        embedding = extract_embedding(img_path)
        dictionary[student_code] = {
            "name": "",
            "embedding": embedding
        }
    return {path.stem:  for path in paths}



def store_embeddings_in_chroma(
    data: Dict[str, Dict[str, Any]],
    collection_name: str,
    persist_directory: str = "./chroma_db",
    filename: Optional[str] = None,
) -> None:
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_or_create_collection(name=collection_name)

    ids = list(data.keys())
    embeddings = [item["embedding"].tolist() for item in data.values()]
    metadatas = [
        {"name": item["name"], **({"filename": filename} if filename else {})}
        for item in data.values()
    ]

    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    
if __name__ == "__main__":
    target_folder = Path("./data/processed/imgs/")
    embeddings_dict = process_images(target_folder)
    # print(embeddings_dict)
