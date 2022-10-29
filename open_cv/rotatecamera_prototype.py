#!/usr/bin/python3
#filename: rotate_camera_until_nav_window_is_dark.py

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
  def __init__(self, w=0,h=0,center_x=0,center_y=0,start_x=0,start_y=0):
    # s_size=pyautogui.size()
    self.w = w # 1920 with one 3840 for two screens
    self.h = h # 1080 
    if w > 2000:
      self.center_x=int(self.w-int(self.w/4)) #get x with two screens
    else:
      self.center_x=int(self.w/2) 
    self.center_y=int(self.h/2)
    self.start_x=self.w-10 #x_right_hand top
    self.start_y=10        #y_right hand top
  
  # def check_for_dark_pixels(self):
  #   colors=pyautogui.pixel(self.x,self.y)
  #   print(f"colors for {self.x},{self.y} are {colors}")
  #   result=pyautogui.pixelMatchesColor(self.x,self.y,(0,0,0), tolerance=60)
  #   return result # True/ False returned 

  def randomize_xy_drag(self):
   #note this can be buggy if an object is encountered on the screen. 
   dest_x=random.randrange(-200,200,30)+self.center_x
   dest_y=random.randrange(-200,200,30)+self.center_y
   #attempting to move a little bit off the center 
   pyautogui.moveTo(self.center_x+(random.randrange(-300,300,100)),self.center_y+(random.randrange(-100,100,5)),duration=0.2)
   scroll_out_value=random.randrange(-15,-3,3) #any number between -15 and -3 
   print (f"Debug - randomize_xy_drag() - scroll_out_value is {scroll_out_value}")
   pyautogui.scroll(scroll_out_value)
   pyautogui.sleep(1)
   pyautogui.mouseDown(button='left')
   pyautogui.moveTo(dest_x,dest_y, duration=0.2)
   pyautogui.mouseUp(button='left')
   pyautogui.sleep(1)

def check_range_for_color_bleed(start_x,start_y,x,y):
  screenshot = ImageGrab.grab(bbox=(start_x,start_y,x,start_y+300)) #specific screen region
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

  print("\n")
  print (f"Info - check_range_for_color_bleed() - threshold_count is {threshold_count}")
  print (f"Info - check_range_for_color_bleed() - count is {count}")
  percent=round(threshold_count*1.00)/count*1.00
  print (f"Info: - check_range_for_color_bleed() - result is {round(percent*100)}")
  if percent*100 > 20: 
    print (f"Debug: - check_range_for_color_bleed() - returning too bright with {percent} bleed.")
    return True  #too bright
  else:
    print (f"Debug: - check_range_for_color_bleed() - returning color is fine.")
    return False #fine
  


#main

my_screensize=pyautogui.size()
w=my_screensize[0] #width  aka x
h=my_screensize[1] #height aka y

nav_bar_too_bright=False
start_x = w-500 #500 pixels in from right edge of monitor 
start_y = 0     #top of screen 
nav_bar_too_bright=check_range_for_color_bleed(start_x,start_y,x=w,y=h)
while nav_bar_too_bright is True:
  a=RotateCamera(w,h)
  a.randomize_xy_drag()
  nav_bar_too_bright=check_range_for_color_bleed(start_x,start_y,x=w,y=h)
  pyautogui.sleep(5)


print('Done.')
