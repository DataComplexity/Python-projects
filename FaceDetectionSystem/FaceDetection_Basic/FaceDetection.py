# FaceDetection_Basic — Simple Image Detection
import cv2
import os

# Configuration
CASCADE_FILE = 'haarcascade_frontalface_default.xml'
IMAGE_FILE = 'test_image.jpg'

def run_detection():
    # 1. Load the cascade
    if not os.path.exists(CASCADE_FILE):
        print(f"Error: {CASCADE_FILE} not found!")
        return

    face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

    # 2. Read the input image
    if not os.path.exists(IMAGE_FILE):
        print(f"Error: {IMAGE_FILE} not found! Please provide a test image.")
        return

    img = cv2.imread(IMAGE_FILE)
    
    # 3. Convert into grayscale (Required for Haar Cascades)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. Detect faces
    # scaleFactor: Parameter specifying how much the image size is reduced at each image scale.
    # minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it.
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    print(f"Found {len(faces)} face(s).")

    # 5. Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # 6. Display the output
    cv2.imshow('Face Detection Results', img)
    print("Press any key to close the window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection()
