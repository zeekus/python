import pyautogui
import time
import random
import sys

def press_w_run(start_time):
 pyautogui.keyDown('w')  # hold down the shift key
 random_delay()
 pyautogui.keyDown('shiftleft')  # hold down the shift key
 random_delay(5)
 pyautogui.keyUp('shiftleft')  # hold down the shift key
 pyautogui.keyUp('w')



def random_delay(n=1):
  if n==0:
    time.sleep( round(random.random() * 9 + 1, 2))
  else:
    time.sleep(round(random.random() * 9 + n, 2))
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
    press_w_run(start_time)
except KeyboardInterrupt:
    print("Program interrupted by Ctrl-c")