'''
Face Tracking with OpenCV and Pan-Tilt controled servos 
    Based on a face detection tutorial on pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

import numpy as np
import cv2
import os
import RPi.GPIO as GPIO

# define servos GPIO
panPin = 27
tiltPin = 17

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

# Defining and initializing globals
global panServoAngle
panServoAngle = 90
global tiltServoAngle
tiltServoAngle =105

# positioning servos at 105-90 degrees
print("\n [INFO] Positioning servos to initial position ==> Press 'ESC' to quit Program \n")
os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))

# Position servos to capture object at center of screen
def servoPosition (x, y):
    global panServoAngle
    global tiltServoAngle
    if (x < 250):
        panServoAngle += 10
        if panServoAngle > 140:
            panServoAngle = 140
        os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
  
    if (x > 300):
        panServoAngle -= 10
        if panServoAngle < 40:
            panServoAngle = 40
        os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))

    if (y < 160):
        tiltServoAngle += 10
        if tiltServoAngle > 140:
            tiltServoAngle = 140
        os.system("python angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
  
    if (y > 210):
        tiltServoAngle -= 10
        if tiltServoAngle < 40:
            tiltServoAngle = 40
        os.system("python angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))


while 1:
    ret, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        servoPosition(int(x+w/2), int(y+h/2))
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        #servoPosition(int(x+w/2), int(y+h/2))
        print (int(x+w/2), int(y+h/2))
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
