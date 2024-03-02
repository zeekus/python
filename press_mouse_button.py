import pyautogui
import time
import random
import sys

def random_delay():
  time.sleep( round(random.random() * 9 + 1, 2))

def press_and_hold_left_mouse_button()
  pyautogui.mouseDown(button='left')
  random_delay()
  pyautogui.mouseUp(button='left')
  
# Loop for 10 seconds
print("waiting for 10 seconds...")
print("open the game you want to test.")
for i in range(10):
    print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
    time.sleep(1)  # Wait for 1 second
print()  # Print a newline after the loop

try: 
  while True
    press_and_hold_left_mouse_button()
    # print("press e")
    # pyautogui.keyDown('e')
    # random_delay()
    # pyautogui.keyUp('e') #release
except KeyboardInterrupt:
    print("Program interrupted by Ctrl-c")

  
