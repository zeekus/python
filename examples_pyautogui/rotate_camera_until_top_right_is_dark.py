
#!/usr/bin/python3
#filename: rotate_camera_until_to_top_right_is_dark.py
#uses pyautogui to map colors on a screen

import time
import os
import pyautogui
import json
import sys
import random
import re
import subprocess  

def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error

def digital_voice(string):
  cmd_echo="echo \'" + str(string) + "\'" #echo string to available digital speak program
  if os.path.exists("/usr/bin/festival"):
    #if festival use it
    cmd_talk="festival --tts"
    status = subprocess.call(cmd_echo + "|" + cmd_talk , shell=True)
  elif os.path.exists("/usr/bin/espeak"):
    cmd_talk="espeak -a 500 -p 1 "
    status = subprocess.call(cmd_echo + "|" + cmd_talk , shell=True)
  else:
     print ("sorry this program will not work without festival or espeak. Please install one.\n")
     sys.exit(1)

def rgb_to_hex(r, g, b):
  return ('{:X}{:X}{:X}').format(r, g, b)

def screen_size():
  size=pyautogui.size()
  #print (f"screen size is {size}")
  x=size[0] #width
  y=size[1] #height
  return x,y

def upper_right():
  x,y=screen_size()
  return x-10,10 # first point 10 pixels from corner

def sample_right_top_of_screen():
  count=0
  mylimit=15
  top_right=upper_right()
  x,y=(top_right[0],top_right[1])
  for c in range (mylimit):
    y=y+20
    x=x-20
    if y> 80:
      y=20
    result = check_for_dark_pixels(x,y)
    if result==True: 
      count=count+1

  if count >= mylimit-2:
    return 0
  else:
    return 1 

def check_for_dark_pixels(x,y):
  colors=pyautogui.pixel(x,y)
  print(f"colors for {x},{y} are {colors}")
  result=pyautogui.pixelMatchesColor(x,y,(0,0,0), tolerance=60)
  return result # True/ False returned 

def drag_me(x,y):
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.mouseUp(button='left')

def randomize_xy_drag(x,y):
   dest_x=random.randrange(-200,200,30)+x
   dest_y=random.randrange(-200,200,30)+y
   drag_me(dest_x,dest_y)

#set focus for the screen
focus_error=focus_window("VE -") #partial name
if focus_error ==1:
  print(f"did not find game window error: {error}")
  sys.exit()

w,h=screen_size() #get screen size
cx=(w/2)
cy=(h/2)
pyautogui.moveTo(cx,cy,.2) #move to center screen 
time.sleep(1)

rotate_camera=sample_right_top_of_screen()
digital_voice(f"rotate_camera is {rotate_camera}")

while( rotate_camera == 1):
  pyautogui.moveTo(cx,cy,.2) #reset on center
  time.sleep(.5)
  randomize_xy_drag(cx,cy)
  rotate_camera=sample_right_top_of_screen()
  digital_voice(f"rotate_camera is {rotate_camera}")

digital_voice("rotation complete")


    
