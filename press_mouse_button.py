import pyautogui
import time
import random
import sys



def random_delay():
  time.sleep( round(random.random() * 9 + 1, 2))

def press_and_hold_left_mouse_button(start_time):
  print("pressing and holding mouse button")
  pyautogui.mouseDown(button='left')
  random_delay()
  pyautogui.mouseUp(button='left')
  end_time=time.time()
  elasped_time=end_time-start_time
  print("releasing mouse button ran for " + str(elasped_time) + " secs")
  
# Loop for 10 seconds
print("waiting for 10 seconds...")
print("open the game you want to test.")
for i in range(10):
    print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
    time.sleep(1)  # Wait for 1 second
print()  # Print a newline after the loop



try: 
  while True:
    start_time=time.time()
    press_and_hold_left_mouse_button(start_time)

    # print("press e")
    # pyautogui.keyDown('e')
    # random_delay()
    # pyautogui.keyUp('e') #release
except KeyboardInterrupt:
    print("Program interrupted by Ctrl-c")

  
