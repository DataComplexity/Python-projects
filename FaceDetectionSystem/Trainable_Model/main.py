"""
ImageOpenCV - Face Recognition System
======================================
An intermediate-level face detection & recognition project using OpenCV.
Supports: dataset collection, model training, and real-time recognition.
"""

import os
import sys

def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║        ImageOpenCV - Face Recognition        ║
║          Powered by OpenCV + LBPH            ║
╚══════════════════════════════════════════════╝
    """)

def print_menu():
    print("""
  [1]  Collect Face Dataset (webcam)
  [2]  Train Recognizer on Dataset
  [3]  Real-Time Face Recognition (webcam)
  [4]  Detect Faces in an Image File
  [5]  Show Dataset Statistics
  [0]  Exit
""")

def main():
    print_banner()

    while True:
        print_menu()
        choice = input("  Select option: ").strip()

        if choice == "1":
            from dataset_collector import collect_dataset
            name = input("  Enter person's name: ").strip()
            if name:
                collect_dataset(name)
            else:
                print("  [!] Name cannot be empty.")

        elif choice == "2":
            from trainer import train_model
            train_model()

        elif choice == "3":
            from face_recognizer import run_live_recognition
            run_live_recognition()

        elif choice == "4":
            path = input("  Enter image file path: ").strip()
            if os.path.exists(path):
                from face_detector import detect_faces_in_image
                detect_faces_in_image(path)
            else:
                print(f"  [!] File not found: {path}")

        elif choice == "5":
            from utils import show_dataset_stats
            show_dataset_stats()

        elif choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        else:
            print("  [!] Invalid option. Try again.")

if __name__ == "__main__":
    main()
