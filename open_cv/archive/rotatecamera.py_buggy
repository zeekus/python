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
    self.x = w # w is an alias for x
    if w > 2000:
      self.center_x=int(self.w-int(self.w/4)) #get x with two screens
    else:
      self.center_x=int(self.w/2) 
    self.center_y=int(self.h/2)
    self.start_x = self.w-500 #500 pixels in from right edge of monitor
    self.start_y=10           #y_right hand top 
    self.debug=debug
  
  def randomize_xy_drag(self):
    if self.center_x > 100 and self.center_y > 100: #bug work aound for two screen bug
     drag_x_start=random.randrange(-200,200,3)+self.center_x
     print(f"debug: rotatecamera.py center is {self.center_x},{self.center_y}") if self.debug >0 else None
     print(f"debug: rotatecamera.py randomize_xy_drag - dest_x: {drag_x_start}") if self.debug >0 else None
     drag_y_start=random.randrange(-200,200,3)+self.center_y 
     print(f"debug: rotatecamera.py randomize_xy_drag - dest_y: {drag_y_start}") if self.debug >0 else None
     drag_x_stop=self.center_x+(random.randrange(-300,300,10))
     drag_y_stop=self.center_y+(random.randrange(-300,300,10))
     print(f"debug: start - random_xy_dest move to {drag_x_start},{drag_y_start}") if self.debug > 0 else None
     pyautogui.moveTo(drag_x_start,drag_y_start,duration=0.2)
     print(f"debug: scroll out")  if self.debug > 0 else None
     scroll_out=random.randrange(5,15,1) #any number between 5-15  
     print (f"Debug - randomize_xy_drag() - scroll_out_value is {scroll_out}") if self.debug > 0 else None
     pyautogui.scroll(scroll_out)
     pyautogui.sleep(1)
     print(f"Press left button down") if self.debug > 0 else None
     pyautogui.mouseDown(button='left')
     print(f"debug drag to: random_xy_dest move to {drag_x_stop}, {drag_y_stop}") if self.debug > 0 else None
     pyautogui.moveTo(drag_x_stop,drag_y_stop, duration=0.2)
     print(f"Press left button up") if self.debug > 0 else None
     pyautogui.mouseUp(button='left')
     pyautogui.sleep(1)
    else:
     print(f"Warning: screen center is too low at {self.center_x},{self.center_y}. We could have scope issue.")

  #def check_range_for_color_bleed(start_x,start_y,x,y):
  def check_range_for_color_bleed(self):
    screenshot = ImageGrab.grab(bbox=(self.start_x,self.start_y,self.x,self.start_y+300)) #specific screen region
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
    if percent > 20: 
      if self.debug>0:
        print (f"Debug: check_range_for_color_bleed() - returning too bright. We should rotate camera.")
      return True  #too bright
    else:
      if self.debug>0:
        print (f"Debug: check_range_for_color_bleed() - returning color is fine. Nothing more to do.")
      return False #fine
