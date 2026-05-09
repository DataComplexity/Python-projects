"""
register.py
-----------
Register a new person by saving their face photo to known_faces/<name>/.
DeepFace builds embeddings automatically when recognize is called.
"""

import cv2
import os
import shutil

KNOWN_FACES_DIR = "known_faces"


def register_from_webcam(name: str):
    """Capture a clear face photo from webcam and save it."""
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    print(f"\n  [+] Registering '{name}' — face the camera clearly.")
    print("  [+] Press SPACE to capture | Q to cancel.\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("  [!] Could not open webcam.")
        return

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 220, 0), 2)

        status = "Face detected — press SPACE to capture" if len(faces) else "No face detected"
        color = (0, 220, 0) if len(faces) else (0, 100, 200)
        cv2.putText(frame, status, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
        cv2.putText(frame, f"Registering: {name}", (12, frame.shape[0] - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 220, 220), 1)

        cv2.imshow("Register - SPACE to capture, Q to cancel", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' ') and len(faces):
            # Count existing images to avoid overwriting
            existing = len(os.listdir(person_dir))
            img_path = os.path.join(person_dir, f"{existing:04d}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"  [✓] Captured and saved: {img_path}")
            # Clear DeepFace cached embeddings so it rebuilds
            _clear_cache()
            break
        elif key == ord('q'):
            print("  [!] Registration cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()


def register_from_image(name: str, image_path: str):
    """Copy an existing image into known_faces/<name>/."""
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    existing = len(os.listdir(person_dir))
    ext = os.path.splitext(image_path)[1]
    dest = os.path.join(person_dir, f"{existing:04d}{ext}")
    shutil.copy2(image_path, dest)
    _clear_cache()
    print(f"  [✓] '{name}' registered from image: {dest}\n")


def _clear_cache():
    """Remove DeepFace's auto-generated embeddings pickle so it rebuilds fresh."""
    import glob
    for f in glob.glob(os.path.join(KNOWN_FACES_DIR, "*.pkl")):
        os.remove(f)
