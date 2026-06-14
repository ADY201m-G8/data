from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from insightface.app import FaceAnalysis
from scipy.io._fast_matrix_market import os

from src import CROPPED_IMG_FOLDER_PATH, RAW_IMG_FOLDER_PATH


def get_face_analyzer(det_size: Tuple[int, int] = (640, 640)) -> FaceAnalysis:
    app = FaceAnalysis(allowed_modules=["detection"])
    app.prepare(ctx_id=0, det_size=det_size)
    return app


def load_image(img_path: Path) -> np.ndarray:
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not open or find the image: {img_path}")
    return img


def extract_face_bbox(app: FaceAnalysis, img: np.ndarray) -> np.ndarray:
    faces = app.get(img)
    if not faces:
        raise ValueError("No face detected in the image.")
    return faces[0].bbox


def compute_square_coords(
    bbox: np.ndarray, img_shape: Tuple[int, int, int]
) -> Tuple[int, int, int, int]:
    h, w, _ = img_shape
    x1, y1, x2, y2 = map(int, bbox)

    box_w: int = x2 - x1
    box_h: int = y2 - y1
    center_x: int = x1 + box_w // 2
    center_y: int = y1 + box_h // 2

    crop_size: int = max(box_w, box_h)
    half_size: int = crop_size // 2

    new_x1: int = center_x - half_size
    new_y1: int = center_y - half_size
    new_x2: int = new_x1 + crop_size
    new_y2: int = new_y1 + crop_size

    if new_x1 < 0:
        new_x2 -= new_x1
        new_x1 = 0
    if new_y1 < 0:
        new_y2 -= new_y1
        new_y1 = 0
    if new_x2 > w:
        new_x1 -= new_x2 - w
        new_x2 = w
    if new_y2 > h:
        new_y1 -= new_y2 - h
        new_y2 = h

    new_x1, new_y1 = max(0, new_x1), max(0, new_y1)
    return new_x1, new_y1, new_x2, new_y2


def crop_image(img: np.ndarray, coords: Tuple[int, int, int, int]) -> np.ndarray:
    x1, y1, x2, y2 = coords
    return img[y1:y2, x1:x2]


def save_image(img: np.ndarray, output_path: str) -> str:
    cv2.imwrite(output_path, img)
    return output_path


def crop_face_pipeline(img_paths: list[Path], output_path: Path) -> None:
    app = get_face_analyzer()

    for img_path in img_paths:
        img: np.ndarray = load_image(img_path)
        bbox: np.ndarray = extract_face_bbox(app, img)
        coords: Tuple[int, int, int, int] = compute_square_coords(bbox, img.shape)
        cropped_img: np.ndarray = crop_image(img, coords)
        save_image(cropped_img, str(output_path / img_path.name))


def main():
    img_paths = list(RAW_IMG_FOLDER_PATH.glob("*"))

    os.makedirs(CROPPED_IMG_FOLDER_PATH, exist_ok=True)

    crop_face_pipeline(img_paths, CROPPED_IMG_FOLDER_PATH)


if __name__ == "__main__":
    main()
