import pyautogui
import random
import time
import os

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
  
  def check_for_dark_pixels(self):
    colors=pyautogui.pixel(self.x,self.y)
    print(f"colors for {self.x},{self.y} are {colors}")
    result=pyautogui.pixelMatchesColor(self.x,self.y,(0,0,0), tolerance=60)
    return result # True/ False returned 

  def randomize_xy_drag(self):
   dest_x=random.randrange(-200,200,30)+self.center_x
   dest_y=random.randrange(-200,200,30)+self.center_y
   pyautogui.moveTo(self.center_x,self.center_y,duration=0.2)
   time.sleep(.2)
   pyautogui.mouseDown(button='left')
   pyautogui.moveTo(dest_x,dest_y, duration=0.2)
   pyautogui.mouseUp(button='left')
   time.sleep(.1)

s_size=pyautogui.size()
w = s_size[0] # 1920 with one 3840 for two screens
h = s_size[1] # 1080 
a=RotateCamera(w,h)
a.randomize_xy_drag()