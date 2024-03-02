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
for i in range(10):
    print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
    time.sleep(1)  # Wait for 1 second

print()  # Print a newline after the loop

for i in range(600):
  # Press the 'E' key
  press_and_hold_left_mouse_button()
  sys.exit()

  print("press e")
  pyautogui.keyDown('e')
  delay=round(random.random() * 9 + 1,2)
  print("waiting: " + delay)
  time.sleep(delay)
  if i % 10 ==0 :
    # Release the 'W' key
    pyautogui.keyUp('e')
  
