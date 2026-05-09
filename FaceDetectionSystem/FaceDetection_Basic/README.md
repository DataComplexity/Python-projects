# FaceDetection_Basic

A foundational computer vision project demonstrating face detection in static images using **Haar Cascade Classifiers**.

## Features

- Detects multiple faces in a single image.
- Draws localized bounding boxes with labels.
- Uses classical OpenCV pre-processing (Grayscale conversion).

## Required Files

- `FaceDetection.py`: The main logic.
- `haarcascade_frontalface_default.xml`: Pre-trained weights ([Source: OpenCV Official GitHub](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)).
- `test_image.jpg`: Sample image for testing.

## How to Run

```bash
python FaceDetection.py
```
