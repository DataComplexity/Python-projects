"""
face_detector.py
----------------
Detect and highlight faces in a static image file.
Optionally runs recognition if a trained model exists.
"""

import cv2
import os
import json

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
MODEL_FILE = "face_model.yml"
LABELS_FILE = "labels.json"
CONFIDENCE_THRESHOLD = 80


def detect_faces_in_image(image_path: str):
    """Detect (and optionally recognize) faces in a given image file."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"  [!] Could not load image: {image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_eq = cv2.equalizeHist(gray)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    faces = face_cascade.detectMultiScale(
        gray_eq, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
    )

    print(f"\n  [+] Image: {image_path}")
    print(f"  [+] Faces detected: {len(faces)}")

    # Try to load recognizer if model exists
    recognizer = None
    label_map = {}
    if os.path.exists(MODEL_FILE) and os.path.exists(LABELS_FILE):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(MODEL_FILE)
        with open(LABELS_FILE, "r") as f:
            raw = json.load(f)
        label_map = {int(k): v for k, v in raw.items()}
        print("  [+] Recognition model loaded. Identifying faces...")
    else:
        print("  [!] No trained model found. Showing detection only.")

    for i, (x, y, w, h) in enumerate(faces):
        name = f"Face {i+1}"
        confidence = 0.0
        color = (255, 140, 0)  # Orange for detection-only

        if recognizer is not None:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label_id, confidence = recognizer.predict(face_roi)
            if confidence < CONFIDENCE_THRESHOLD:
                name = label_map.get(label_id, f"Face {i+1}")
                color = (0, 200, 0)
            else:
                name = "Unknown"
                color = (0, 0, 220)

        # Draw bounding box
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

        # Label with background
        label = name if recognizer is None else f"{name} ({confidence:.1f})"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
        cv2.rectangle(img, (x, y - th - 12), (x + tw + 8, y), color, -1)
        cv2.putText(img, label, (x + 4, y - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        print(f"    Face {i+1}: {name}  | Position: ({x},{y})  Size: {w}x{h}" +
              (f"  Confidence: {confidence:.1f}" if recognizer else ""))

    # Save annotated output
    base, ext = os.path.splitext(os.path.basename(image_path))
    out_path = f"{base}_detected{ext}"
    cv2.imwrite(out_path, img)
    print(f"\n  [✓] Annotated image saved: {out_path}")

    # Display
    cv2.imshow("Face Detection Result - Press any key to close", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print()
