#!/usr/bin/python3
#filename: find_image_on_screen.py
#description: Provide image and find similar image on the screen. Note without python-opencv2 this is unreliable. 
#runtime is about .20 - .30 seconds

import pyautogui
import time
import os # to get pwd
now=later=time.time()
path=os.getcwd()
myfile=(path + "/messages/app01.png")
print("myfile for the image target is " + myfile )
image_target=pyautogui.locateOnScreen(myfile, confidence=0.9) #needs python-opencv2 returns object

now_after_run=time.time()
if image_target != None:
  
  print (type(image_target))
  print (str(image_target))
  x,y=pyautogui.locateCenterOnScreen(myfile, confidence=0.9) #needs python-opencv2 object can't be NONE for this to run
  
  print ("image target center on screen at " + str((x,y)) )
  pyautogui.moveTo(image_target)
  pyautogui.moveTo(x,y) #center

else:
  print ("image target not found on screen.")


print ("runtime: " + str(now_after_run-now))
