import time
import os
import pyautogui
import json
import sys
import random
import re
import subprocess
from rotatecamera import RotateCamera #import rotate camera class
from calibration import Calibration 
from findimage import FindImage
from parsegamelog import ParseGameLog



def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    #print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error

def click_button(x,y,speed,description,debug=1):
  match = re.search('button', description)
  if match:
    x,y=randomize_xy(x,y) #randomize click location 1-2 pixels each time
  pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
  if debug > 0:
    print("Debug: click_button() - '" + description + "' center at: (" +  "x: " + str(x) + ",y: " + str(y) + ")" )
  x1,y1=pyautogui.position()
  if x1==x and y1==y: 
     pyautogui.click()
  else:
    print("Warning: mouse moved.")

focus_error=focus_window("VE -") #partial name open game window
path=os.getcwd() #get current working directory
button_json_file =(f"{path}/buttons/buttons.json")
w,h=pyautogui.size()
myval=Calibration(w,h) #sets up screen refpoints and return as myval object
yellow_result=None
yellow_result,yellow_image=FindImage.search_for_image_and_return_location(button_json_file,"yellow gate icon",myval.navbar_ltop,myval.bottom_right)
click_button(yellow_result[0]+2,yellow_result[1]+2,1,"clicking yellow icon")
time.sleep(5)

while True: 
    #pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
    yellow_result=None
    pyautogui.moveTo(myval.navbar_ltop[0],myval.navbar_ltop[1],1, pyautogui.easeOutQuad)    #work around to prevent bug - when start location is the same as the target this fails. 
    yellow_result,yellow_image=FindImage.search_for_image_and_return_location(button_json_file,"yellow gate icon",myval.navbar_ltop,myval.bottom_right)
    print(myval.navbar_ltop)
    click_button(yellow_result[0]+2,yellow_result[1]+2,1,"clicking yellow icon")
    print(f"yellow_result:{yellow_result}")
    time.sleep(5)

