"""
utils.py
--------
Utility helpers: dataset statistics, folder setup, etc.
"""

import os
import json

DATASET_DIR = "dataset"
MODEL_FILE = "face_model.yml"
LABELS_FILE = "labels.json"


def show_dataset_stats():
    """Print a summary of the dataset and model status."""
    print("\n  ── Dataset Statistics ──────────────────────────────")

    if not os.path.exists(DATASET_DIR):
        print("  [!] No dataset directory found.")
    else:
        persons = [p for p in os.listdir(DATASET_DIR)
                   if os.path.isdir(os.path.join(DATASET_DIR, p))]
        if not persons:
            print("  [!] Dataset directory is empty.")
        else:
            total_samples = 0
            for person in sorted(persons):
                person_path = os.path.join(DATASET_DIR, person)
                count = len([f for f in os.listdir(person_path)
                             if f.lower().endswith((".jpg", ".jpeg", ".png"))])
                total_samples += count
                bar = "█" * min(count // 2, 30)
                print(f"  {person:<20} {bar}  ({count} samples)")
            print(f"\n  Total: {len(persons)} person(s), {total_samples} samples")

    print("\n  ── Model Status ────────────────────────────────────")
    if os.path.exists(MODEL_FILE):
        size_kb = os.path.getsize(MODEL_FILE) // 1024
        print(f"  [✓] Model file : {MODEL_FILE}  ({size_kb} KB)")
    else:
        print(f"  [✗] Model file : Not found (run training first)")

    if os.path.exists(LABELS_FILE):
        with open(LABELS_FILE) as f:
            labels = json.load(f)
        print(f"  [✓] Labels file: {LABELS_FILE}  ({len(labels)} classes)")
        for uid, name in labels.items():
            print(f"      [{uid}] {name}")
    else:
        print(f"  [✗] Labels file: Not found")

    print()
