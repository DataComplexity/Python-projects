# FaceRecognitionSystem (Pretrained Model)

Real-time face recognition using the **DeepFace** framework with pretrained models (default: **VGG-Face**). This version uses deep learning embeddings for high accuracy without requiring direct training on your part.

---

## Tech Stack

| Library | Role |
|---|---|
| `deepface` | Framework for Face Verification & Recognition |
| `OpenCV` | Image capturing, webcam feed, and drawing |
| `TensorFlow` | Backend engine for DeepFace models |
| `VGG-Face` | Pretrained CNN model (default) |

---

## Terminal Error Fix
If you see the error: **`ValueError: idate_for_keras3()`** or **`run pip install tf-keras`**, run the following command:

```bash
pip install tf-keras
```
*Complexity Note: TensorFlow 2.16+ uses Keras 3 by default, but DeepFace requires the Keras 2 behavior provided by `tf-keras`.*

---

## Project Structure

```
Pretrained_Model/
├── main.py            ← Entry point (Menu system)
├── register.py        ← Capture/add photos to database
├── recognizer.py      ← Live webcam recognition logic
├── detector.py        ← Static image analysis
├── database.py        ← DB management
├── known_faces/       ← Directory containing labeled face folders
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
pip install tf-keras  # Required for recent TF versions
python main.py
```

---

## How It Works

1. **Registration**: You provide a photo or capture one via webcam. It is saved in `known_faces/<name>/`.
2. **Representation**: DeepFace uses a CNN (VGG-Face) to extract a high-dimensional embedding (vector) from the face.
3. **Verification**: When recognize is called, it compares the current face's vector against the registered vectors using **Cosine Similarity**.
4. **Distance Threshold**: If the similarity distance is `< 0.4`, the person is identified.

---

## Tuning (recognizer.py)

| Parameter | Default | Effect |
|---|---|---|
| `MODEL` | `"VGG-Face"` | Try `Facenet`, `ArcFace`, or `OpenFace` |
| `DISTANCE_METRIC` | `"cosine"` | `euclidean` or `euclidean_l2` |
| `PROCESS_EVERY` | `20` | Lower = more frequent recognition (heavier CPU/GPU) |
