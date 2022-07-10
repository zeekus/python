

import time
import os
import pyautogui



def click(button):

  time.sleep(5)
  p=pyautogui.locateCenterOnScreen(button,confidence=0.9)
  if p == None:
    print ("no image found on screen")
  else:
    print("moving mouse to:" +  str(p))
    pyautogui.moveTo(p[0],p[1],2, pyautogui.easeOutQuad)    # start fast, end slow
    print("clicking mouse at:" +  str(p))
    pyautogui.click(x=p[0], y=p[1])

def docking_sequence(docking_message,dock_icon):

  #click on dock button
  click(dock_icon)

  docking_image=None
  while docking_image == None:
    time.sleep(0.5)
    #wait until docking image appears
    docking_image=pyautogui.locateOnScreen(docking_message, confidence=0.95)

  print("dock sequence complete")

path=os.getcwd()
dock_icon=(path + "/buttons/__dock.png")

docking_messages=[]
docking_messages.append(path + "/messages/docking.png")
docking_messages.append(path + "/messages/docking0.png")

docking_sequence(docking_messages[1],dock_icon)
