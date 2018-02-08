'''
BGR to HSV Color Conversion
    Create by Henry Dang ==> See the tutorial here:
    https://henrydangprg.com/2016/06/26/color-detection-in-python-with-opencv/
Adapted by Marcelo Rovai - MJRoBot.org @8Feb18
'''

import sys
import numpy as np
import cv2
 
blue = sys.argv[1]
green = sys.argv[2]
red = sys.argv[3]  
 
color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
 
hue = hsv_color[0][0][0]
 
print("Lower bound is :"),
print("[" + str(hue-10) + ", 100, 100]\n")
 
print("Upper bound is :"),
print("[" + str(hue + 10) + ", 255, 255]")
