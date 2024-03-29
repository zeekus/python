#!/usr/bin/python
#filename: automated_scanner.py

import pyautogui
import tkinter as tk
from tkinter import TclError
import time
import re
import os
import random
import subprocess

def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    #print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error

def reset_scan_location(x,y):
  pyautogui.moveTo(x,y)
  pyautogui.click(x,y)

def select_all_and_copy_to_clipboard(x,y):
  # reset_scan_location(x,y) #too slow with this
  # time.sleep(1)  
  with pyautogui.hold('ctrlleft'):
    pyautogui.press('a')
    pyautogui.press('c')

def check_clipboard():
    root.withdraw()
    try: 
       result=root.selection_get(selection="CLIPBOARD")
       ##print("debug: entries in clipboard")
    except TclError:
       # handle the error the way you see fit
       ##print("debug: empty clipboard")
       root.clipboard_append(".")
       result=root.selection_get(selection="CLIPBOARD")
       
    ##print("debug: result is :" + result )
    return result


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
   #ignore non threating objects
   ignore_type=["Athanor", "Raitaru", "Astrahus", "Fortizar", "Control Tower", "Mobile Depot", "Velator", "Prospect"]
   for ignore_string in ignore_type:
       if re.search(ignore_string,string):
           return True
   return False

def espeak_warn(string):
    os.system("espeak " + string + " on grid" )

def is_clipboard_empty():
    try:
      root.selection_get(selection="CLIPBOARD")
    except TclError: 
        return True #clipboard empty
    return False #clipboard not empty

#open game window 
focus_error=focus_window("VE -") #partial name open game window
if focus_error ==1:
  print(f"did not find game window error: {focus_error}")
  sys.exit()

#user action needed. We need to move to the location of the scanner.
print("move your cursor to game window or this will crash")
for x in range(1,5,1):
  print(".",end='',flush=True)
  time.sleep(1)
print()
x,y=pyautogui.position()
print("current location is " + "X:" + str(x) + "," + "Y:" + str(y))

count=0
root = tk.Tk() #first session

while True:
    
    pyautogui.typewrite('v') #press v for scan
    select_all_and_copy_to_clipboard(x,y)
    text=check_clipboard()
    list_of_text=re.split(r"[~\r\n]+", text)
    count=1
    obj_count=0
    if (len(text)) > 10:
      print(f"debug1: raw text from clipboard:\n'{text}'")
      for line in list_of_text:
        #break line up into an array delimiated by tabs
        text_fields=re.split(r"[\t]+",line)
        obj_count=obj_count+1
        ignore=ignore_type(text_fields[2]) 
        if ignore is False:
          #check if friendly
          friendly=check_friendly(text_fields[1]) 
          if friendly is False:
            espeak_warn(text_fields[2]) #warn user of new ship
            print(str(count) + ":" + line)
            count=count+1
      print("debug: objects " +  str(obj_count))

    random_delay=random.randint(1,3)
    random_delay= random_delay + random.randint(0,100)*.01

    time.sleep(random_delay)
    x1,y2=pyautogui.position()
    if x==x1 and y==y2:
      #clear clipboard after every scan
      root.withdraw() #hide tk interface
      root.clipboard_clear() #clear clipboard
      root.update()  #force update
      root.destroy() #destroy session 
      root=tk.Tk() #restart tk session
      if is_clipboard_empty()==True: 
        root.clipboard_append("") #starter text
      pass
    else:
      print("The mouse moved. Breaking out of the game.")
      break
