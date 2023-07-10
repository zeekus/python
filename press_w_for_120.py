import pyautogui
import time

# Loop for 10 seconds
for i in range(10):
    print(".", end="", flush=True)  # Print a dot without a newline and flush the output buffer
    time.sleep(1)  # Wait for 1 second

print()  # Print a newline after the loop

# Press the 'W' key
pyautogui.keyDown('w')

# Wait for 120 seconds
time.sleep(120)

# Release the 'W' key
pyautogui.keyUp('w')
