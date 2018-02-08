'''
Color Detection in Python with OpenCV
    Create by Henry Dang ==> See the tutorial here:
    https://henrydangprg.com/2016/06/26/color-detection-in-python-with-opencv/
Adapted by Marcelo Rovai - MJRoBot.org @8Feb18
'''

import cv2
import numpy as np
 
img = cv2.imread('yellow_object.JPG', 1) # The 1 means we want the image in BGR, and not in grayscale
# resize imag to 20% in each axis
img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
# convert BGR image to a HSV image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

# NumPy to create arrays to hold lower and upper range (got from bgr_hsv_converter.py)
lower_range = np.array([24, 100, 100], dtype=np.uint8) # The “dtype = np.uint8” simply means that it will have the data type an 8 bit integer
upper_range = np.array([44, 255, 255], dtype=np.uint8)

# create a mask for image
mask = cv2.inRange(hsv, lower_range, upper_range)

# display both the mask and the image side-by-side
cv2.imshow('mask',mask)
cv2.imshow('image', img)

# wait to user to press [ ESC ]
while(1):
  k = cv2.waitKey(0)
  if(k == 27):
    break
 
cv2.destroyAllWindows()
python