import pyautogui
import time
import random
import sys

def press_and_hold_left_mouse_button(start_time):
  print("pressing and holding mouse button")
  pyautogui.mouseDown(button='left')
  wait10(5)
  pyautogui.mouseUp(button='left')
  end_time=time.time()
  elasped_time=end_time-start_time
  print("releasing mouse button ran for " + str(elasped_time) + " secs")

def move_forward_w():
 pyautogui.keyDown('w')  # hold down the shift key
 time.sleep(1)
 pyautogui.keyUp('w')

def random_delay():
  time.sleep( round(random.random() * 9 + 1, 2))
  
def wait10(n=10):
 # Loop for 10 seconds
 print("waiting for 10 seconds...")
 print("open the game you want to test.")
 for i in range(n):
  print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
  time.sleep(1)  # Wait for 1 second
 print()  # Print a newline after the loop

def down_arrow(n=22):
    pyautogui.keyDown('shift')  # hold down the shift key
    for x in range(n):
      pyautogui.press('down')     # press the down arrow key
    pyautogui.keyUp('shift')    # release the shift key

def up_arrow(n=22):
    pyautogui.keyDown('shift')  # hold down the shift key
    for x in range(n):
      pyautogui.press('up')     # press the up arrow key
    pyautogui.keyUp('shift')    # release the shift key

wait10()
try: 
  while True:
    pyautogui.click()  # click the mouse
    st=time.time()
    x,y=pyautogui.position()
    print(pyautogui.position())
    press_and_hold_left_mouse_button(st)
    down_arrow()
    print(pyautogui.position())
    press_and_hold_left_mouse_button(st)
    up_arrow()
    st=time.time()
    move_forward_w()
except KeyboardInterrupt:
    print("Program interrupted by Ctrl-c")