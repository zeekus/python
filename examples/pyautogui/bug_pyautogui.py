#filename: bug_pyautogui.py
#description: attempting to replicate a bug

import pyautogui


while True:
    r=pyautogui.locateOnScreen("./stars3.png",confidence=0.80)
    print(f'image is at {r[0]},{r[1]}')
    pyautogui.moveTo(r[0],r[1])
    pyautogui.sleep(2)

    
