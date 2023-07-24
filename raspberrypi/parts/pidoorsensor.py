import RPi.GPIO as GPIO
import time
#from Simpon Prickett
#ref: https://github.com/simonprickett/pidoorsensor/blob/master/pidoorsensor1.py
#howto: 1. connect PCM whatver and a ground colors or polarity doesn't matter
#when the door opens it should register as open. 
#Used GPIO 21 and Ground 39 when testing.

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	if GPIO.input(21):
		print "Door open!"
	else:
		print "Door closed!"
	
	time.sleep(0.1)