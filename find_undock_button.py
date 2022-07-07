#!/usr/bin/python3
import pyautogui
import time
now=later=time.time()
buttonlocation = pyautogui.locateOnScreen('/home/ted/Documents/git/python/image_lib/undock2.png',grayscale=True)
now_after_run=time.time()
#pyautogui.click('/home/ted/Documents/git/python/image_lib/undock2.png')
print (buttonlocation)
print (str(now_after_run-now))
