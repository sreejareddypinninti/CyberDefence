import cv2
import os

# Store in a project-relative directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data_stored")

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        os.makedirs(DATA_DIR, exist_ok=True)
        cv2.imwrite(os.path.join(DATA_DIR, 'Intruder.jpg'), frame)
    else:
        print("Failed to capture frame")
else:
    print("Could not open webcam")

cap.release()