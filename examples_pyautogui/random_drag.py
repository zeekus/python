#! python3
#filename: random_drag.py
#description: move_window in random location from current mouse location
import pyautogui, sys, time, random

def randomize_xy_drag(x,y):
   dest_x=random.randrange(-133,133,30)+x
   dest_y=random.randrange(-133,133,30)+y
   drag_me(dest_x,dest_y)

def drag_me(x,y):
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x, y, 2, pyautogui.easeOutQuad)
    pyautogui.mouseUp(button='left')

while True:
  x,y = pyautogui.position()
  print( 'X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) )
  print('\n')
  randomize_xy_drag(x,y)
  time.sleep(5)
  
