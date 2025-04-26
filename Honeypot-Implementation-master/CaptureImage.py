import cv2
import os

# Update directory to project-specific storage
DATA_DIR = r"C:\Users\koosuru_vardhini\tasks\honeypot\Honeypot-Implementation-master\data_stored"

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        os.makedirs(DATA_DIR, exist_ok=True)
        os.chdir(DATA_DIR)
        cv2.imwrite('Intruder.jpg', frame)
    else:
        print("Failed to capture frame")
else:
    print("Could not open webcam")

cap.release()