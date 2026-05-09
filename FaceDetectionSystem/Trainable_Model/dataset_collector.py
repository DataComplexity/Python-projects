"""
dataset_collector.py
--------------------
Captures face samples from the webcam and saves them to the dataset folder.
Each person gets a subfolder: dataset/<name>/
"""

import cv2
import os

DATASET_DIR = "dataset"
SAMPLES_PER_PERSON = 50   # Number of face samples to capture
FRAME_DELAY_MS = 100       # Milliseconds between captures

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def collect_dataset(name: str):
    """Capture face images from webcam and store in dataset/<name>/"""

    person_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    # Count existing samples so we don't overwrite
    existing = len([f for f in os.listdir(person_dir) if f.endswith(".jpg")])
    print(f"\n  [+] Collecting samples for '{name}'")
    print(f"  [+] Existing samples: {existing}")
    print(f"  [+] Will capture {SAMPLES_PER_PERSON} new samples.")
    print("  [+] Press 'Q' to quit early.\n")

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("  [!] Could not open webcam.")
        return

    count = 0
    sample_index = existing

    while count < SAMPLES_PER_PERSON:
        ret, frame = cap.read()
        if not ret:
            print("  [!] Failed to read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            # Save the face ROI (Region of Interest)
            face_roi = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (200, 200))

            filename = os.path.join(person_dir, f"{sample_index:04d}.jpg")
            cv2.imwrite(filename, face_resized)
            sample_index += 1
            count += 1

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Sample {count}/{SAMPLES_PER_PERSON}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Progress bar overlay
        progress = int((count / SAMPLES_PER_PERSON) * frame.shape[1])
        cv2.rectangle(frame, (0, frame.shape[0] - 15), (progress, frame.shape[0]), (0, 200, 0), -1)
        cv2.putText(frame, f"Collecting: {name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Dataset Collector - Press Q to quit", frame)

        key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
        if key == ord('q'):
            print("  [!] Collection cancelled by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"\n  [✓] Collected {count} samples for '{name}'.")
    print(f"  [✓] Saved to: {person_dir}\n")
