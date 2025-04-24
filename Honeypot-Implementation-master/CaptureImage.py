import cv2
import os
import time
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)
    
if cap.isOpened():
    ret, frame = cap.read()
    print(ret)
    print(frame)
else:
    ret = False

img1 = frame

directory = r"C:/UsersADMIN/Downloads/Honeypot/Honeypot-Implementation-master/data_stored"
os.chdir(directory)
print(os.listdir(directory)) 
filename = 'Intruder.jpg'
cv2.imwrite(filename, img1) 


cap.release()
