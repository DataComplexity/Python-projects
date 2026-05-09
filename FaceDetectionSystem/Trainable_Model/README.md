# ImageOpenCV — Face Recognition System

A face detection and recognition project using **OpenCV** and the **LBPH (Local Binary Patterns Histograms)** algorithm. No deep learning required — pure classical computer vision.

---

## Features

| Feature | Description |
|---|---|
| Dataset Collector | Capture face samples from your webcam |
| Model Trainer | Train LBPH recognizer on collected data |
| Live Recognition | Real-time recognition via webcam |
| Image Detection | Detect + recognize faces in any image file |
| Dataset Stats | View sample counts and model status |

---

## Project Structure

```
ImageOpenCV/
├── main.py               # Entry point (interactive menu)
├── dataset_collector.py  # Webcam-based face data collection
├── trainer.py            # LBPH model training
├── face_recognizer.py    # Real-time webcam recognition
├── face_detector.py      # Static image face detection/recognition
├── utils.py              # Dataset statistics & helpers
├── requirements.txt      # Python dependencies
│
├── dataset/              # Auto-created: face samples
│   ├── Alice/
│   │   ├── 0000.jpg
│   │   └── ...
│   └── Bob/
│
├── face_model.yml        # Auto-created: trained LBPH model
└── labels.json           # Auto-created: ID → name mapping
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py
```

> **Important:** Use `opencv-contrib-python` (not just `opencv-python`)  
> because the LBPH recognizer lives in the `cv2.face` contrib module.

---

## Workflow

### Step 1 — Collect Dataset

- Choose option `[1]` and enter the person's name.
- Sit in front of the webcam; the system captures **50 face samples** automatically.
- Repeat for each person you want to recognize.

### Step 2 — Train the Model

- Choose option `[2]`.
- The LBPH recognizer trains on all collected samples.
- Model is saved to `face_model.yml`.

### Step 3 — Recognize

- Choose option `[3]` for live webcam recognition.
- **Green box** = known person | **Red box** = Unknown

---

## How It Works

```
Webcam Frame
     │
     ▼
Grayscale + Histogram Equalization
     │
     ▼
Haar Cascade → Detect Face ROI
     │
     ▼
Resize to 200×200
     │
     ▼
LBPH Recognizer → predict(face_roi)
     │
     ├── confidence < threshold  → Label with name
     └── confidence >= threshold → "Unknown"
```

**LBPH** divides the face image into a grid of cells and computes Local Binary Patterns (texture descriptors) for each cell, then compares the histograms against stored training histograms.

---

## Tuning

| Parameter | File | Default | Effect |
|---|---|---|---|
| `SAMPLES_PER_PERSON` | `dataset_collector.py` | 50 | More = better accuracy |
| `CONFIDENCE_THRESHOLD` | `face_recognizer.py` | 80 | Lower = stricter matching |
| `minNeighbors` | detector calls | 5 | Higher = fewer false positives |

---

## Controls (Webcam Modes)

| Key | Action |
|---|---|
| `Q` | Quit |
| `S` | Save screenshot (recognition mode) |

---

## Dependencies

- `opencv-python` — core CV functions
- `opencv-contrib-python` — LBPH face recognizer (`cv2.face`)
- `numpy` — array handling
