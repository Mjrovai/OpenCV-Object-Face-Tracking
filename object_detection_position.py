'''
Object detection and tracking with OpenCV
    ==> Turning a LED on detection and
    ==> Real Time tracking with Pan-Tilt servos 

    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/

Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

# initialize GPIOs
redLed = 21
panPin = 27
tiltPin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
colorLower = (24, 100, 100)
colorUpper = (44, 255, 255)

# Start with LED off
GPIO.output(redLed, GPIO.LOW)
ledOn = False

# Initialize servos at 90-90 position
global panServoAngle
panServoAngle = 90
global tiltServoAngle
tiltServoAngle =90

# positioning servos
print("\n Positioning servos to initial position ==> Press 'q' to quit Program \n")
os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))

# Position servos to capture object at center of screen
def servoPosition (x, y):
    global panServoAngle
    global tiltServoAngle
    if (x < 220):
        panServoAngle += 10
        if panServoAngle > 140:
            panServoAngle = 140
        os.system("python angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
  
    if (x > 280):
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

# loop over the frames from the video stream
while True:
	# grab the next frame from the video stream, Invert 180o, resize the
	# frame, and convert it to the HSV color space
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	frame = imutils.rotate(frame, angle=180)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the object color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			servoPosition(int(x), int(y)) 
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			# if the led is not already on, turn the LED on
			if not ledOn:
				GPIO.output(redLed, GPIO.HIGH)
				ledOn = True

	# if the ball is not detected, turn the LED off
	elif ledOn:
		GPIO.output(redLed, GPIO.LOW)
		ledOn = False

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("\n Exiting Program and cleanup stuff \n")
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()