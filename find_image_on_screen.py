#!/usr/bin/python3
#filename: find_image_on_screen.py
#description: Provide image and find similar image on the screen. Note without python-opencv2 this is unreliable. 
#runtime is about .20 - .30 seconds

import pyautogui
import time
now=later=time.time()
#image_location = pyautogui.locateOnScreen('/home/ted/Documents/git/python/image_lib/undock2.png',grayscale=True)
#image_location = pyautogui.locateOnScreen('/home/ted/Documents/git/python/image_lib/undock.png', confidence=0.9) #needs python-opencv2
#image_location = pyautogui.locateOnScreen('/home/ted/Documents/git/python/image_lib/undock2.png', confidence=0.9) #needs python-opencv2
image_location = pyautogui.locateOnScreen('/home/ted/Documents/git/python/image_lib/app01.png', confidence=0.9) #needs python-opencv2
now_after_run=time.time()
#pyautogui.click('/home/ted/Documents/git/python/image_lib/undock2.png')
print (image_location)
print (str(now_after_run-now))
