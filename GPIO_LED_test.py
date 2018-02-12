'''
Testing GPIO with a LED
    To run enter with parameters ==> $ python GPIO_LED_test.py <#GPIO> <frequency in seconds>
    Example: python GPIO_LED_test.py 21 1
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

import sys
import time
import RPi.GPIO as GPIO

# initialize GPIO and variables
redLed = int(sys.argv[1])
freq = int(sys.argv[2])
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)
GPIO.setwarnings(False)

print("\n [INFO] Blinking LED (5 times) connected at GPIO {0} at every {1} second(s)".format(redLed, freq))
for i in range(5):
    GPIO.output(redLed, GPIO.LOW)
    time.sleep(freq)
    GPIO.output(redLed, GPIO.HIGH)
    time.sleep(freq)

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
GPIO.cleanup()