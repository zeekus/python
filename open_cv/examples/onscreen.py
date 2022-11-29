#!/usr/bin/python

import pyautogui
from calibration import Calibration

w,h=pyautogui.size()
myval=Calibration(w,h)

pyautogui.moveTo(-1,-1)

x,y=pyautogui.position()
try: 
    if pyautogui.onScreen(x,y)==True:
      print(f"x:{x},y:{y}")
    else:
      print(f"old location: x:{x},y:{y}")
      pyautogui.moveTo(myval.bottom_right[0],myval.bottom_right[1])
      x,y=pyautogui.position()
      print(f"new location x:{x},y:{y}")

except:
    print("FailSafe Exception")
