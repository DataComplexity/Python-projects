"""
detector.py
-----------
Recognize faces in a static image file using DeepFace.
Annotates and saves the result as <filename>_result.jpg
"""

import cv2
import os
import numpy as np

KNOWN_FACES_DIR = "known_faces"
MODEL = "VGG-Face"
DETECTOR = "skip"
DISTANCE_METRIC = "cosine"
THRESHOLD = 0.4


def detect_in_image(image_path: str):
    if not os.path.exists(KNOWN_FACES_DIR) or not os.listdir(KNOWN_FACES_DIR):
        print("\n  [!] No registered faces. Please register someone first.\n")
        return

    from deepface import DeepFace

    print(f"\n  [+] Analyzing: {image_path}")
    frame = cv2.imread(image_path)

    try:
        df_list = DeepFace.find(
            img_path=image_path,
            db_path=KNOWN_FACES_DIR,
            model_name=MODEL,
            detector_backend=DETECTOR,
            distance_metric=DISTANCE_METRIC,
            silent=True,
            enforce_detection=False,
            align=False,
        )
        print(f"  [debug] df returned {len(df_list)} results")
    except Exception as e:
        print(f"  [!] DeepFace error: {e}")
        return

    # DeepFace.find returns one dataframe per detected face
    print(f"  [+] Faces detected: {len(df_list)}")

    for i, df in enumerate(df_list):
        if df is None or len(df) == 0:
            print(f"    Face {i+1}: Unknown")
            continue

        top = df.iloc[0]
        dist = top[f"{MODEL}_{DISTANCE_METRIC}"]

        # Get bounding box if available
        x = int(top.get("source_x", 0))
        y = int(top.get("source_y", 0))
        w = int(top.get("source_w", 100))
        h = int(top.get("source_h", 100))

        if dist < THRESHOLD:
            name = os.path.basename(os.path.dirname(top["identity"]))
            confidence = 1 - dist
            color = (20, 200, 80)
            label = f"{name}  ({confidence:.0%})"
            print(f"    Face {i+1}: {name}  |  confidence: {confidence:.0%}")
        else:
            name = "Unknown"
            color = (0, 60, 200)
            label = "Unknown"
            print(f"    Face {i+1}: Unknown")

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
        cv2.rectangle(frame, (x, y - th - 12), (x + tw + 8, y), color, -1)
        cv2.putText(frame, label, (x + 4, y - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    base, ext = os.path.splitext(os.path.basename(image_path))
    out = f"{base}_result{ext}"
    cv2.imwrite(out, frame)
    print(f"\n  [✓] Saved: {out}")

    cv2.imshow("Result - press any key to close", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print()
