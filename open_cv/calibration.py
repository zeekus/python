#filename: calibration.py
#description: class holding screen calibration functions

import os,pyautogui

class Calibration:
  #variables
  screen_left_t =[0,0] #top left of screen
  screen_rgt_b  =[0,0] #bottom right of screen
  nav_bar_t     =[0,0] #top of nav bar
  nav_bar_b     =[0,0] #bottom of nav bar
  a_center      =[0,0] #align/approach center
  jt_center     =[0,0] #jump/to center
  jd_center     =[0,0] #jump/dock button center
  i_icon        =[0,0,0,0] #icon start x,y dims
  screen_center =[0,0]

  def __init__(self, w=0,h=0):
    self.w = w # 1920 with one 3840 for two screens
    self.h = h # 1080 
    if w > 2000:
      self.screen_left_t =[int(self.w/2),0] #top left of screen
      self.screen_center=[int(self.w/4),int(self.h/2)] #get x with two screens
    else:
      self.screen_left_t =[0,0] #top left of screen
      self.screen_center=[int(self.w/2),int(self.h/2)] #get x with two screens

    self.screen_rgt_b=[self.w,self.h]
    self.path=os.getcwd() #get current working directory 
    self.buttons_folder =self.path + "/buttons/"
    self.message_folder =self.path + "/message/"
    self.button_json_file =(self.buttons_folder + "buttons.json")  #description of button images
    self.message_json_file=(self.message_folder + "messages.json") #description of message images

  def display_variables(self):
    print(self)

my_screensize=pyautogui.size()
w=my_screensize[0] #width  aka x
h=my_screensize[1] #height aka y
a=calibration(w,h)
a.display_variables
