"""
face_recognizer.py
------------------
Real-time face recognition using the trained LBPH model.
Draws bounding boxes, name labels, and confidence scores on the webcam feed.
"""

import cv2
import os
import json

MODEL_FILE = "face_model.yml"
LABELS_FILE = "labels.json"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

CONFIDENCE_THRESHOLD = 80   # Below this = "Known", above = "Unknown"


def load_recognizer():
    """Load trained model and label map. Returns (recognizer, label_map) or None."""
    if not os.path.exists(MODEL_FILE):
        print(f"  [!] Model file '{MODEL_FILE}' not found. Please train first.")
        return None, None
    if not os.path.exists(LABELS_FILE):
        print(f"  [!] Labels file '{LABELS_FILE}' not found. Please train first.")
        return None, None

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_FILE)

    with open(LABELS_FILE, "r") as f:
        raw = json.load(f)
    label_map = {int(k): v for k, v in raw.items()}

    return recognizer, label_map


def draw_prediction(frame, x, y, w, h, name, confidence):
    """Draw bounding box and label for a detected/recognized face."""
    if name == "Unknown":
        color = (0, 0, 220)    # Red for unknown
    else:
        color = (0, 200, 0)    # Green for known

    # Box
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    # Background for text
    label = f"{name}  ({confidence:.1f})"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
    cv2.rectangle(frame, (x, y - th - 12), (x + tw + 8, y), color, -1)
    cv2.putText(frame, label, (x + 4, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)


def run_live_recognition():
    """Webcam loop: detect and recognize faces in real-time."""
    recognizer, label_map = load_recognizer()
    if recognizer is None:
        return

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("  [!] Could not open webcam.")
        return

    print("\n  [+] Starting real-time recognition...")
    print("  [+] Press 'Q' to quit, 'S' to save a screenshot.\n")

    screenshot_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Equalize histogram for better detection in varied lighting
        gray_eq = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(
            gray_eq, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
        )

        face_count = len(faces)

        for (x, y, w, h) in faces:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label_id, confidence = recognizer.predict(face_roi)

            if confidence < CONFIDENCE_THRESHOLD:
                name = label_map.get(label_id, "Unknown")
            else:
                name = "Unknown"
                label_id = -1

            draw_prediction(frame, x, y, w, h, name, confidence)

        # HUD overlay
        cv2.putText(frame, f"Faces detected: {face_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, "Q: Quit  |  S: Screenshot", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Face Recognition - Live", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_count += 1
            fname = f"screenshot_{screenshot_count:03d}.jpg"
            cv2.imwrite(fname, frame)
            print(f"  [✓] Screenshot saved: {fname}")

    cap.release()
    cv2.destroyAllWindows()
    print("  [+] Recognition stopped.\n")
