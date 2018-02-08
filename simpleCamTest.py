'''
Simple Cam Test - BGR and Gray
    Create by pythonprogramming.net ==> See the tutorial here:
    https://pythonprogramming.net/loading-video-python-opencv-tutorial
Adapted by Marcelo Rovai - MJRoBot.org @8Feb18
'''

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
 
while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
