# FaceDetectionSystem — Face Recognition Trilogy

This repository contains three distinct implementations of Face Detection and Recognition, showcasing the evolution from simple image processing to complex deep learning.

## Projects in this Suite

### 1. [Basic Detection (Haar Cascades)](./FaceDetection_Basic/)
- **Algorithm**: Viola-Jones Framework.
- **Library**: OpenCV.
- **Core Concept**: Detecting faces in static images using pre-trained XML features.
- **Best For**: Beginners learning the basics of image coordinates and pre-processing.

### 2. [Trainable Model (Classical CV)](./Trainable_Model/)

- **Algorithm**: LBPH (Local Binary Patterns Histograms).
- **Library**: OpenCV (Contrib module).
- **Core Concept**: Manual dataset collection and model training on a local machine.
- **Best For**: Understanding the fundamentals of image histograms and bitwise operations.

### 3. [Pretrained Model (Deep Learning)](./Pretrained_Model/)

- **Framework**: DeepFace (VGG-Face, Facenet, or ResNet).
- **Library**: TensorFlow, Keras, OpenCV.
- **Core Concept**: Using high-dimensional face embeddings for zero-shot recognition.
- **Best For**: High-accuracy, production-ready scenarios without manual training.

---

## Main Tech Stack

- **Languages**: Python
- **Libraries**: OpenCV, DeepFace, TensorFlow, NumPy
- **Models**: VGG-Face, LBPH, Haar Cascades

## Getting Started

Each sub-project has its own `README.md` and `requirements.txt`.

1. Choose a model folder.
2. Install dependencies.
3. Run `main.py` to launch the interactive menu.
