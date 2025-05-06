import cv2
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data_stored")
LOG_FILE = os.path.join(DATA_DIR, "capture_image.log")

def log_error(msg):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        os.makedirs(DATA_DIR, exist_ok=True)
        cv2.imwrite(os.path.join(DATA_DIR, 'Intruder.jpg'), frame)
    else:
        log_error("Failed to capture frame")
else:
    log_error("Could not open webcam")

cap.release()