#! python3
#filename: random_drag_until_green_pixel.py
#description: move_window in random location from current mouse location 
#use open google earth at https://earth.google.com/web 
#position earth in center of screen the program will turn the image until a green pixel is detected. 

import pyautogui, sys, time, random
import cv2 as cv

def randomize_xy_drag(x,y):
   dest_x=random.randrange(-200,200,30)+x
   dest_y=random.randrange(-200,200,30)+y
   drag_me(dest_x,dest_y)

def drag_me(x,y):
    pyautogui.mouseDown(button='left')
    #pyautogui.moveTo(x, y, duration=0.1, pyautogui.easeOutQuad)
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.mouseUp(button='left')

def find_dark_green_pixel(x,y): #trees
  colors=pyautogui.pixel(x,y)
  result=pyautogui.pixelMatchesColor(x,y,(67,102,123), tolerance=20)
  return result

#record starting location 
start_x, start_y = pyautogui.position() #start position

count=0
print(f"click on the window to preform drags.")
time.sleep(1)
green_result=False
while(True and count<5 and green_result is False):
  pyautogui.moveTo(start_x,start_y,duration=.3)
  green_result=find_dark_green_pixel(start_x,start_y)
  #pyautogui.moveTo(start_x,start_y,duration=.3, pyautogui.easeOutQuad)
  pyautogui.click()
  x,y = pyautogui.position()
  colors=pyautogui.pixel(x,y)
  print(f"{colors}")
  print( ''+ str(count).rjust(1) + ':X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) )
  print('\n')
  randomize_xy_drag(x,y)
  count = count+1
  time.sleep(5)

