import pyautogui
import time

# Loop for 10 seconds
for i in range(10):
    print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
    time.sleep(1)  # Wait for 1 second

print()  # Print a newline after the loop

for i in range(600):
  # Press the 'E' key
  pyautogui.keyDown('e')
  random_sleep = random.randinit(1,10)
  time.sleep(random_sleep)
  if i % 10 ==0 :
    # Release the 'W' key
    pyautogui.keyUp('e')
  
