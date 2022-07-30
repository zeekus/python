#!/usr/bin/python
#filename: automated_scanner.py

import pyautogui
import tkinter as tk
import time
import re
import os

def reset_scan_location(x,y):
  pyautogui.moveTo(x,y)
  pyautogui.click(x,y)

def select_and_copy_all():
  pyautogui.keyDown('ctrlleft')
  pyautogui.press('a')
  pyautogui.press('c')
  pyautogui.keyUp('ctrlleft')

def get_game_clipboard():
    select_and_copy_all()
    root = tk.Tk()
    root.withdraw()
    return root.clipboard_get()

def ignore_type(string):
   ignore_type=["Athanor", "Raitaru", "Astrahus", "Fortizar", "Control Tower"]
   for ignore_string in ignore_type:
       if re.search(ignore_string,string):
           return True
   return False

def espeak_warn(string):
    os.system("espeak " + string + " on grid" )

print("move your cursor to game window or this will crash")
time.sleep(10)
x,y=pyautogui.position()
print("current location is " + "X:" + str(x) + "," + "Y:" + str(y))


while True:
    reset_scan_location(x,y)
    #press v for the scanner
    pyautogui.typewrite('v') 
    text=get_game_clipboard()
    list_of_text=re.split(r"[~\r\n]+", text)
    #print("simple list")
    #print(list_of_text)
    count=1
    for line in list_of_text:
        #break line up into an array delimiated by tabs
        text_fields=re.split(r"[\t]+",line)
        ignore=ignore_type(text_fields[2]) 
        if ignore is False:
          espeak_warn(text_fields[2]) #warn user of new ship
          print(str(count) + ":" + line)
          count=count+1

    time.sleep(5)
