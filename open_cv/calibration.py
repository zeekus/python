#filename: calibration.py
#description: class holding screen calibration functions

import os,pyautogui

"""A class for calibrating the basic screen limits.
   
    Attributes:
        w (int): width of the screen.
        h (int): height of the screen 

    Sets variables:
      myvals
        - top_left      - x,y location for the top corner of the screen
        - bottom_right  - x,y location for the bottom corner of the screen 
        - navbar_ltop   - x,y location of scan start for navbar
        - navbar_rbot   - x,y location of scan stop for navbar
"""

class Calibration:
  def __init__(self, w=0,h=0):
    self.w = w # 1920 with one 3840 for two screens
    self.h = h # 1080
    self.debug=0 # global for debugs
    print(f"Calibration Screen Size: {w},{h}")
    if w > 2000:
      self.top_left =[int(self.w/2)+3,3] #top left of screen if two screens 
    else:
      self.top_left =[3,3] #top left of screen if one screen 

    self.bottom_right=[self.w-3,self.h-3] #offset by 3 pixels
    self.navbar_ltop =[self.bottom_right[0]-450,30]
    self.navbar_rbot =[self.bottom_right[0]-10,150] 
    print(f"From Calibration self.top_left: {self.top_left} self.bottom_right: {self.bottom_right}")
    
  def display_variables(self):
    """
    A function for debugging, the limits.
    This may be needed if more than 2 screens are used. 
    """
    print(f"path is {self.path}")
    print(f"moving mouse to 'top_left' at      {self.top_left}")
    pyautogui.moveTo(self.top_left[0],self.top_left[1],2)
    pyautogui.sleep(1)
    print(f"moving mouse to 'bottom_right' at  {self.bottom_right}")
    pyautogui.moveTo(self.bottom_right[0],self.bottom_right[1],2)
    pyautogui.sleep(1)
    print(f"moving mouse to 'screen_center' at {self.screen_center}")
    pyautogui.moveTo(self.screen_center[0],self.screen_center[1],1)  
    pyautogui.sleep(1)
    print(f"moving mouse to 'navbar_rtop' at   {self.navbar_ltop}")
    pyautogui.moveTo(self.navbar_ltop[0],self.navbar_ltop[1],1)
    pyautogui.sleep(1)
    print(f"moving mouse to 'navbar_rbot' at   {self.navbar_rbot}")
    pyautogui.moveTo(self.navbar_rbot[0],self.navbar_rbot[1],1)
    pyautogui.sleep(1)

