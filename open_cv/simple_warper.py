

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


#click on jump button
path=os.getcwd()
jumpicon=(path + "/buttons/__jump.png")
click(jumpicon)

jumping_message=None

while jumping_message == None:
  time.sleep(1)

  #wait until Jumping messaging appears
  jump_message=(path + "/messages/jump2.png")
  jumping_message=pyautogui.locateOnScreen(jump_message, confidence=0.9)


print("jump sequence complete")

