import time
from pathlib import Path
from typing import Any, List, NamedTuple, Tuple

import chromadb
import cv2
import numpy as np
from insightface.app import FaceAnalysis

from src import CHROMA_DB_FOLDER_PATH, EMBEDDING_MODEL


class FaceMatch(NamedTuple):
    bbox: Tuple[int, int, int, int]
    identity: str


class AppConfig(NamedTuple):
    collection: Any
    face_analyzer: FaceAnalysis
    distance_threshold: float = 0.5
    margin_ratio_threshold: float = 0.8


def init_resources(db_path: Path, collection_name: str) -> AppConfig:
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name=collection_name)

    app = FaceAnalysis(
        name=EMBEDDING_MODEL,
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    )
    app.prepare(ctx_id=0, det_size=(640, 640))

    return AppConfig(collection=collection, face_analyzer=app)


def query_identity(
    embedding: List[float],
    collection: chromadb.Collection,
    threshold: float,
    margin_threshold: float,
) -> str:
    results = collection.query(query_embeddings=[embedding], n_results=4)
    if not results or not results["distances"] or len(results["distances"][0]) == 0:
        return "?"

    distances = results["distances"][0]
    match_id = results["ids"][0][0]

    if distances[0] < threshold:
        print(f"L1 {match_id} {distances[0]}")
        return match_id

    margin_ratio = (
        (distances[0] / distances[1])
        + (distances[0] / distances[2])
        + (distances[0] / distances[3])
    ) / 3
    if margin_ratio < margin_threshold:
        print(f"L2 {match_id} {distances} {margin_ratio}")
        return match_id

    return "?"


def process_face(
    face: Any, collection: Any, threshold: float, margin_threshold: float
) -> FaceMatch:
    x1, y1, x2, y2 = face.bbox.astype(int)
    embedding = face.normed_embedding.tolist()
    identity = query_identity(embedding, collection, threshold, margin_threshold)
    return FaceMatch(bbox=(x1, y1, x2, y2), identity=identity)


def draw_match(frame: np.ndarray, match: FaceMatch) -> None:
    x1, y1, x2, y2 = match.bbox

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(
        frame,
        match.identity,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )


def process_frame(frame: np.ndarray, config: AppConfig) -> np.ndarray:
    t1 = time.perf_counter()

    detected_faces = config.face_analyzer.get(frame)

    t2 = time.perf_counter()

    matches = [
        process_face(
            face,
            config.collection,
            config.distance_threshold,
            config.margin_ratio_threshold,
        )
        for face in detected_faces
    ]

    t3 = time.perf_counter()

    output_frame = frame
    for match in matches:
        draw_match(output_frame, match)

    t4 = time.perf_counter()
    print(f"faces {t2 - t1} | search {t3 - t2} | draw {t4 - t3}")

    return output_frame


def main():
    config = init_resources(db_path=CHROMA_DB_FOLDER_PATH, collection_name="all")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame, config)

        cv2.imshow("Face Recognition", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
