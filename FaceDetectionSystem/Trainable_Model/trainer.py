"""
trainer.py
----------
Trains an LBPH (Local Binary Patterns Histograms) face recognizer
on the collected dataset and saves the model + label map.
"""

import cv2
import os
import json
import numpy as np

DATASET_DIR = "dataset"
MODEL_FILE = "face_model.yml"
LABELS_FILE = "labels.json"


def load_training_data():
    """
    Walk dataset directory and load face images + integer labels.
    Returns: (faces, labels, label_map)
      - faces     : list of grayscale numpy arrays
      - labels    : list of int IDs
      - label_map : dict mapping int ID -> person name
    """
    faces = []
    labels = []
    label_map = {}
    current_id = 0

    if not os.path.exists(DATASET_DIR):
        return faces, labels, label_map

    for person_name in sorted(os.listdir(DATASET_DIR)):
        person_path = os.path.join(DATASET_DIR, person_name)
        if not os.path.isdir(person_path):
            continue

        label_map[current_id] = person_name
        print(f"  Loading '{person_name}' (ID={current_id}) ...", end=" ")

        count = 0
        for img_file in os.listdir(person_path):
            if not img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            img_path = os.path.join(person_path, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img_resized = cv2.resize(img, (200, 200))
            faces.append(img_resized)
            labels.append(current_id)
            count += 1

        print(f"{count} samples")
        current_id += 1

    return faces, labels, label_map


def train_model():
    """Train LBPH recognizer and save the model + label map."""
    print("\n  [+] Loading training data...\n")
    faces, labels, label_map = load_training_data()

    if len(faces) == 0:
        print("  [!] No training data found. Please collect a dataset first.")
        return

    if len(label_map) < 1:
        print("  [!] Need at least 1 person in the dataset.")
        return

    print(f"\n  [+] Training on {len(faces)} samples for {len(label_map)} person(s)...")

    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
        threshold=80.0   # Confidence threshold (lower = stricter)
    )
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_FILE)

    with open(LABELS_FILE, "w") as f:
        # JSON keys must be strings
        json.dump({str(k): v for k, v in label_map.items()}, f, indent=2)

    print(f"  [✓] Model saved to '{MODEL_FILE}'")
    print(f"  [✓] Labels saved to '{LABELS_FILE}'")
    print(f"\n  Summary:")
    for uid, name in label_map.items():
        count = labels.count(uid)
        print(f"    [{uid}] {name}: {count} samples")
    print()
