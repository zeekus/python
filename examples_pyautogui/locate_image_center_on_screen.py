import time
import pyautogui
time.sleep(5)
p=pyautogui.locateCenterOnScreen('/home/ted/jump_icon.jpg',confidence=0.9)
if p == None:
    print ("no image found on screen")
else:
    print(str(p))
    pyautogui.moveTo(p[0],p[1],2, pyautogui.easeOutQuad)    # start fast, end slow
    pyautogui.click(x=p[0], y=p[1])

