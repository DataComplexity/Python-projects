"""
database.py
-----------
Manages the known_faces/ folder.
DeepFace uses the folder structure directly — no pickle needed from our side.
eg...:
known_faces/
  Alice/
    0000.jpg
  Bob/
    0000.jpg
"""

import os
import shutil
import glob

KNOWN_FACES_DIR = "known_faces"


def list_people():
    print()
    if not os.path.exists(KNOWN_FACES_DIR):
        print("  [!] No registered faces yet.\n")
        return

    people = [p for p in os.listdir(KNOWN_FACES_DIR)
              if os.path.isdir(os.path.join(KNOWN_FACES_DIR, p))]

    if not people:
        print("  [!] No registered faces yet.\n")
        return

    print("  ── Registered People ───────────────────────────")
    for name in sorted(people):
        count = len([f for f in os.listdir(os.path.join(KNOWN_FACES_DIR, name))
                     if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        print(f"  {name:<25} {count} image(s)")
    print(f"\n  Total: {len(people)} person(s)\n")


def remove_person(name: str):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    if os.path.exists(person_dir):
        shutil.rmtree(person_dir)
        # Clear DeepFace cache
        for f in glob.glob(os.path.join(KNOWN_FACES_DIR, "*.pkl")):
            os.remove(f)
        print(f"  [✓] '{name}' removed.\n")
    else:
        print(f"  [!] '{name}' not found.\n")
