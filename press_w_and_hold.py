import pyautogui
import time
import random
import sys

def press_and_hold_w(start_time):
 pyautogui.keyDown('w')  # hold down the shift key
 random_delay()
 pyautogui.keyUp('w')

def random_delay():
  time.sleep( round(random.random() * 9 + 1, 2))
  
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
    press_and_hold_w(start_time)

    # print("press e")
    # pyautogui.keyDown('e')
    # random_delay()
    # pyautogui.keyUp('e') #release
except KeyboardInterrupt:
    print("Program interrupted by Ctrl-c")

  
