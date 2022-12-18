#!/usr/bin/python3
#filename: rotatecamera.py

import cv2 as cv
import numpy as np
import random
import os
from PIL import ImageGrab
from time import time
import pyautogui
import sys
#results: 26 - 40FPS on Linux on laptop
#import pydirectinput #ref uses assembly references for keyboard and mousemovements.
#import mss #seems to be faster with multi-platform support # https://github.com/BoboTiG/python-mss
#ref https://www.youtube.com/watch?v=WymCpVUPWQ4
#ref https://pypi.org/project/PyDirectInput/

# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time=time()

class RotateCamera:
  #define your monitor width and height
  
  #constructor
  def __init__(self, w=0,h=0,center_x=0,center_y=0,start_x=0,start_y=0,debug=0):
    # s_size=pyautogui.size()
    self.w = w # 1920 with one 3840 for two screens
    self.h = h # 1080 
    self.start_x = self.w-500 #500 pixels in from right edge of monitor
    self.start_y=10           #y_right hand top 
    ##self.debug=debug 
    self.debug=1 #force debug 1
    #print(f"debug rotatecamera.py - contstructor:{w},{h}")
  
  def randomize_xy_drag(self,start_x=0,start_y=0,stop_x=0,stop_y=0):
    count=0
    #print(f"debug rotatecamera.py - randomize_xy_drag :{self.w},{self.h}")
    if self.w > 2000: #large screen could mean 2
     center_x=int(self.w-int(self.w/4)) #get x with two screens
     center_y=int(self.h/2)
    else: #normal screen 
     center_x=int(self.w/2) 
     center_y=int(self.h/2)
    print(f"Debug rotatecamera.py - center x,y :{center_x},{center_y}") if self.debug > 0 else None 

    #note this can be buggy if an object is encountered on the screen. 
    while start_x<=0 or start_y<=0:
      start_x=center_x-random.randrange(25,150,1)
      start_y=center_y-random.randrange(25,150,1)
      stop_x=random.randrange(50,150,1)+center_x
      stop_y=random.randrange(50,150,1)+center_y
      #print(".",end='',flush=True)
      count=count+1
      if self.debug >0:
        print(f"Debug: rotatecamera.py - random_xy_drag: {count}: start_x: {start_x}, start_y: {start_y} stop_x: {stop_x}, stop_y: {stop_y}")
      if count>15:
        sys.exit()

    #print(f"* debug: randomize_xy_drag: start:[{start_x},{start_y}] end:[{stop_x},{stop_y}]")

    #attempting to move a little bit off the center 
    #print(f"debug: random_xy_start move to [{start_x},{start_y}]")
    if pyautogui.onScreen(start_x,start_y) == True and pyautogui.onScreen(stop_x,start_y) == True:
      pyautogui.moveTo(start_x,start_y,duration=0.2)
      scroll_out=random.randrange(5,15,1) #any number between 5-15  
      pyautogui.scroll(scroll_out)
      pyautogui.sleep(2)
      pyautogui.mouseDown(button='left')
      print(f"Debug- rotate camera start: x:{start_x},y:{start_y} stop x:{stop_x},y:{stop_y}") if self.debug > 0 else None
      pyautogui.moveTo(stop_x,stop_y,duration=0.2)
      pyautogui.mouseUp(button='left')
      pyautogui.sleep(1)
    else:
      print(f"Warning OFFSCREEN  rotate camera start: x:{start_x},y:{start_y} stop x:{stop_x},y:{stop_y}")

  #def check_range_for_color_bleed(start_x,start_y,x,y):
  def check_range_for_color_bleed(self):
    screenshot = ImageGrab.grab(bbox=(self.start_x,self.start_y,self.w,self.start_y+300)) #specific screen region
    screenshot=np.array(screenshot)#convert screenshot to numpy array 
    screenshot= cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) #opencv RGB color conversion
    #drop alpha channel data from the image
    screenshot = screenshot[...,:3] #numpy slice - slows down things.
    #fix type errors
    #final convert https://github.com/opencv/opencv/issues/#14866#issuecomment-580207109
    screenshot = np.ascontiguousarray(screenshot)
    count=1
    threshold_count=0
    for index,x in np.ndenumerate(screenshot):
      #print(f"location: {index},value: {x},entry count: {count}")
      if x > 60 : #color greater than 60 it may be too bright
        threshold_count+=1
      count+=1 #count the fields in the np array

    #print("\n")
    #print (f"Debug: - check_range_for_color_bleed() - threshold_count is {threshold_count}")
    #print (f"Debug: - check_range_for_color_bleed() - count is {count}")
    percent=round(100*(threshold_count*1.00)/count*1.00)
    if self.debug>0:
      print (f"Debug: - check_range_for_color_bleed() - bleed result is {percent}")
    if percent > 60: 
      if self.debug>0:
        print (f"Debug: check_range_for_color_bleed() - returning too bright. We should rotate camera.")
      return True  #too bright
    else:
      if self.debug>0:
        print (f"Debug: check_range_for_color_bleed() - returning color is fine. Nothing more to do.")
      return False #fine
