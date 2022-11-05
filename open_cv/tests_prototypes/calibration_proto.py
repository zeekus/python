#filename: calibration.py
#description: class holding screen calibration functions

import os,pyautogui

class Calibration:
  def __init__(self, w=0,h=0):
    self.w = w # 1920 with one 3840 for two screens
    self.h = h # 1080
    self.debug=1 
    print(f"{w},{h}")
    if w > 2000:
      self.top_left =[int(self.w/2)+3,3] #top left of screen
      self.screen_center=[(w-int(.5*self.w/2)),int(self.h/2)] #get center of second screen 
    else:
      self.top_left =[3,3] #top left of screen
      self.screen_center=[int((self.w/2-3)),int((self.h/2)-3)] #get x with two screens

    self.bottom_right=[self.w-3,self.h-3] #offset by 3 pixels
    self.path=os.getcwd() #get current working directory 
    self.buttons_folder =self.path + "/buttons/"
    self.message_folder =self.path + "/message/"
    self.button_json_file =(self.buttons_folder + "buttons.json")  #description of button images
    self.message_json_file=(self.message_folder + "messages.json") #description of message images
    self.navbar_ltop =[self.bottom_right[0]-410,30]
    self.navbar_rbot =[self.bottom_right[0]-10,150] 
    
  def display_variables(self):
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

w,h=pyautogui.size()
myval=Calibration(w,h) #sets up scan points
if myval.debug==1:
  myval.display_variables()
print(f"myval.navbar_rbot:{myval.navbar_rbot}")

