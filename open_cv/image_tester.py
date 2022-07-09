#!/usr/bin/python3
#filename: image_tester.py
#description: loop though an array and identify the images as they come on the screen. 
#goal: it to find out what sequence we are in.
#runtime is about .20 - .30 seconds

import pyautogui
import time
import os,subprocess # to get pwd and interact with espeak

def find_target_image_on_screen(myfile):
  #using opencv find the image target on the screen
  now=later=time.time()
  print("myfile for the image target is " + myfile ) 
  image_target=pyautogui.locateOnScreen(myfile, confidence=0.9) #needs python-opencv2 returns object
  now_after_run=time.time()
  print ("runtime1 xy: " + str(now_after_run-now))
  if image_target != None: 
    return 1 #found
  else:
    return 0 #not found

def get_image_center_cords(myfile):  
  image_exists=find_target_image_on_screen(myfile)

  if image_exists == 1: 
    now=later=time.time()
    x,y=pyautogui.locateCenterOnScreen(myfile, confidence=0.9) #needs python-opencv2 object can't be NONE for this to run
    now_after_run2=time.time()
    print ("runtime2 xy: " + str(now_after_run2-now))
    print ("image target center on screen at " + str((x,y)) )
    # pyautogui.moveTo(image_target)
    # pyautogui.moveTo(x,y) #center of image 
    return x,y
  else:
    print ("image target not found on screen.")
    return 0,0

def computer_speak(message):
  if os.path.exists("/usr/bin/festival"):
    mytalk=("festival --tts")
    subprocess.call("echo " + message + "|" + mytalk, shell=True)
  elif os.path.exists("/usr/bin/espeak"):
    mytalk=("/usr/bin/espeak")
    subprocess.call("echo " + message + "|" + mytalk, shell=True)
  else:
    print("sorry this program needs either espeake or festival to talk.")
    sys.exit(1)

  
path=os.getcwd()
myfile=(path + "/messages/app01.png")
get_image_center_cords(myfile)
result=find_target_image_on_screen(myfile)
if result == 1:
  message=("approaching")
  computer_speak(message)

