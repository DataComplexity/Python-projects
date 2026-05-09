"""
FaceRecognitionSystem
======================
Pretrained face recognition using DeepFace (VGG-Face model) + OpenCV.
No training required — register a face once, recognize instantly.
"""

import os
import sys

def print_banner():
    print("""
╔══════════════════════════════════════════════════╗
║          FaceRecognitionSystem                   ║
║       DeepFace  |  OpenCV  |  VGG-Face           ║
╚══════════════════════════════════════════════════╝
    """)

def print_menu():
    print("""
  [1]  Register a new person (webcam)
  [2]  Register from an image file
  [3]  Live face recognition (webcam)
  [4]  Recognize faces in an image file
  [5]  List registered people
  [6]  Remove a person
  [0]  Exit
""")

def main():
    print_banner()

    while True:
        print_menu()
        choice = input("  Select option: ").strip()

        if choice == "1":
            from register import register_from_webcam
            name = input("  Enter person's name: ").strip()
            if name:
                register_from_webcam(name)
            else:
                print("  [!] Name cannot be empty.")

        elif choice == "2":
            from register import register_from_image
            name = input("  Enter person's name: ").strip()
            path = input("  Enter image file path: ").strip()
            if name and os.path.exists(path):
                register_from_image(name, path)
            else:
                print("  [!] Invalid name or file not found.")

        elif choice == "3":
            from recognizer import run_live_recognition
            run_live_recognition()

        elif choice == "4":
            path = input("  Enter image file path: ").strip()
            if os.path.exists(path):
                from detector import detect_in_image
                detect_in_image(path)
            else:
                print(f"  [!] File not found: {path}")

        elif choice == "5":
            from database import list_people
            list_people()

        elif choice == "6":
            from database import remove_person
            name = input("  Enter name to remove: ").strip()
            if name:
                remove_person(name)

        elif choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        else:
            print("  [!] Invalid option. Try again.")

if __name__ == "__main__":
    main()
