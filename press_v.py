import time
import pyautogui
import random
#import tkinter as tk
import clipboard

def getClipboardText():
    pyautogui.hotkey('ctrl_l','c') 
    return clipboard.paste()

#click_on_eve_screen
print("click on eve screen")
time.sleep(10)

while True: 
    print("pressing v")
    pyautogui.typewrite('v') #press v for scanner
    #print("reading clipboard")
    #text=getClipboardText()
    #print("clipboard says :" + text)
    random_delay=random.randint(1,7)
    random_delay= random_delay + random.randint(0,100)*.01
    print("sleeping for " + str(round(random_delay,2)) + " seconds")
    time.sleep(random_delay)

