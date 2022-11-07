#!/usr/bin/python3
#filename: press_ok.py
#description: when ok appears on the screen press ok.
#requirements: a png image of the OK button.

import pyautogui
my_button=None
while True:
 pyautogui.sleep(10) # go to sleep
 my_button= pyautogui.locateOnScreen('ok_button.png') #gets location to ok button
 if my_ok_button !=None:
   x,y = pyautogui.center(my_button) #button center
   pyautogui.click(x, y) #click on center of 'ok' button
