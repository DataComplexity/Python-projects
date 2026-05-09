"""
recognizer.py
-------------
Real-time face recognition using DeepFace + OpenCV webcam feed.
Captures a frame, saves it temporarily, runs DeepFace.find()
against the known_faces/ database, draws results.
"""

import cv2
import os
import tempfile
import numpy as np

KNOWN_FACES_DIR = "known_faces"
MODEL = "VGG-Face"           # Options: VGG-Face, Facenet, ArcFace, DeepFace
DETECTOR = "opencv"          # Fast detector backend
DISTANCE_METRIC = "cosine"
PROCESS_EVERY = 5            # Run DeepFace every 5 frames (increased frequency)
DEBUG = False                # Silenced logs


def run_live_recognition():
    if not os.path.exists(KNOWN_FACES_DIR) or not os.listdir(KNOWN_FACES_DIR):
        print("\n  [!] No registered faces. Please register someone first.\n")
        return

    # Import here so startup is fast
    from deepface import DeepFace

    print(f"\n  [+] Loading model: {MODEL} ...")
    print("  [+] Press Q to quit | S to screenshot\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("  [!] Could not open webcam.")
        return

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    frame_count = 0
    last_results = []    # Cache: list of (x, y, w, h, name, confidence)
    screenshot_n = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % PROCESS_EVERY == 0:
            last_results = _recognize_frame(frame, face_cascade, DeepFace)

        # Draw cached results on every frame
        for (x, y, w, h, name, conf) in last_results:
            color = (20, 200, 80) if name != "Unknown" else (0, 60, 200)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            label = f"{name}  ({conf:.0%})" if name != "Unknown" else "Unknown"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
            cv2.rectangle(frame, (x, y - th - 12), (x + tw + 8, y), color, -1)
            cv2.putText(frame, label, (x + 4, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        cv2.putText(frame, f"Faces: {len(last_results)}", (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)
        cv2.putText(frame, "Q: Quit  S: Screenshot", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

        cv2.imshow("FaceRecognitionSystem - Live", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_n += 1
            fname = f"screenshot_{screenshot_n:03d}.jpg"
            cv2.imwrite(fname, frame)
            print(f"  [✓] Screenshot: {fname}")

    cap.release()
    cv2.destroyAllWindows()
    print("  [+] Stopped.\n")


def _recognize_frame(frame, face_cascade, DeepFace):
    """Detect faces and run DeepFace.find() on each one."""
    results = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
            cv2.imwrite(tmp_path, face_img)

        try:
            df = DeepFace.find(
                img_path=tmp_path,
                db_path=KNOWN_FACES_DIR,
                model_name=MODEL,
                detector_backend=DETECTOR,
                distance_metric=DISTANCE_METRIC,
                silent=True,
                enforce_detection=False,
            )

            if len(df) > 0 and not df[0].empty:
                top = df[0].iloc[0]
                
                # Dynamically find the distance column (contains 'distance', 'cosine', 'euclidean', or 'vgg-face')
                dist_cols = [c for c in df[0].columns if any(x in c.lower() for x in ['distance', DISTANCE_METRIC.lower(), MODEL.lower()])]
                if not dist_cols:
                    if DEBUG: print(f"  [error] Could not find distance column in: {df[0].columns.tolist()}")
                    results.append((x, y, w, h, "Unknown", 0.0))
                    continue
                
                dist_col = dist_cols[0]
                dist = top[dist_col]
                # Cosine distance: 0 = identical, 1 = opposite
                # Threshold ~0.4 works well for VGG-Face cosine
                if DEBUG:
                    print(f"  [debug] distance={dist:.4f}  identity={top['identity']}")
                if dist < 0.45: # Slightly loosened threshold
                    # Extract name from path: known_faces/Name/img.jpg
                    identity = top["identity"]
                    name = os.path.basename(os.path.dirname(identity))
                    confidence = 1 - dist
                    results.append((x, y, w, h, name, confidence))
                else:
                    results.append((x, y, w, h, "Unknown", 0.0))
            else:
                results.append((x, y, w, h, "Unknown", 0.0))

        except Exception as e:
            if DEBUG:
                print(f"  [error] DeepFace error: {e}")
            results.append((x, y, w, h, "Unknown", 0.0))
        finally:
            os.unlink(tmp_path)

    return results
