from pathlib import Path

import chromadb
import cv2
from insightface.app import FaceAnalysis

from src import CHROMA_DB_FOLDER_PATH, EMBEDDING_MODEL, EXECUTION_PROVIDERS

TARGET_IMAGE_PATH = Path("./src/tests/HE204320.jpg")

app = FaceAnalysis(name=EMBEDDING_MODEL, providers=EXECUTION_PROVIDERS)
app.prepare(ctx_id=0, det_size=(224, 224))

client = chromadb.PersistentClient(path=str(CHROMA_DB_FOLDER_PATH))
collection = client.get_collection(name="all")


def main():
    img = cv2.imread(str(TARGET_IMAGE_PATH))
    faces = app.get(img)

    if not faces:
        raise ValueError(f"No face detected in {TARGET_IMAGE_PATH}")

    target_embedding = faces[0].embedding.tolist()

    results = collection.query(
        query_embeddings=[target_embedding],
        n_results=collection.count(),
        include=["metadatas", "distances"],
    )

    if not results["distances"] or not results["metadatas"]:
        return

    print(f"{'ID':<20} | {'Distance':<10} | {'Cosine Similarity':<18} | {'Metadata'}")
    print("-" * 80)

    ids = results["ids"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    for item_id, distance, metadata in zip(ids, distances, metadatas):
        similarity = 1.0 - distance
        print(f"{item_id:<20} | {distance:<10.4f} | {similarity:<18.4f} | {metadata}")


if __name__ == "__main__":
    main()
