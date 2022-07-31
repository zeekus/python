#!/usr/bin/python
#filename: automated_scanner.py

import pyautogui
import tkinter as tk
import time
import re
import os
import random

def reset_scan_location(x,y):
  pyautogui.moveTo(x,y)
  pyautogui.click(x,y)

def select_all_and_copy():
  with pyautogui.hold('ctrlleft'):
    pyautogui.press('a')
    pyautogui.press('c')

def get_game_clipboard():
    select_all_and_copy()
    root = tk.Tk()
    root.withdraw()
    if len(root.clipboard_get())>0:
      return root.clipboard_get()
    else: 
      return ""

def check_friendly(string):
  #example friendly ships use 3 letter call sign followed by 3 numbers that add up to 15
  name_fields=re.split(r" +", string) 
  #name_fields=['ZRI', '618', 'Slacker']
  pattern=re.compile("[a-zA-Z]+")#letter pattern
  #print("check for a three letter call sign with a-z patern match")
  if len(name_fields[0]) == 3 and len(name_fields[1]) ==3 and pattern.fullmatch(name_fields[0]) is not None:
       #3 letter call sign found
       #find sum of 3 number signifier
       my_sum=(sum(int(a) for a in re.findall(r'\d',name_fields[1])))
       if len(name_fields[1])==3 and my_sum ==15:
          return True
       
  else:
    return False


def ignore_type(string):
   ignore_type=["Athanor", "Raitaru", "Astrahus", "Fortizar", "Control Tower", "Mobile Depot", "Velator", "Prospect"]
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

count=0


while True:
    #if count % 10:
    #  reset_scan_location(x,y)

    #press v for the scanner

    pyautogui.typewrite('v') 
    text=get_game_clipboard()
    #print("original of text size:" + str(len(text)))
    list_of_text=re.split(r"[~\r\n]+", text)
    #print("simple list")
    #print(list_of_text)
    count=1
    if text != "":
      for line in list_of_text:
        #break line up into an array delimiated by tabs
        text_fields=re.split(r"[\t]+",line)
        ignore=ignore_type(text_fields[2]) 
        if ignore is False:
          #check if friendly
          friendly=check_friendly(text_fields[1]) 
          if friendly is False:
            espeak_warn(text_fields[2]) #warn user of new ship
            print(str(count) + ":" + line)
            count=count+1

    random_delay=random.randint(1,7)
    random_delay= random_delay + random.randint(0,100)*.01

    time.sleep(random_delay)

