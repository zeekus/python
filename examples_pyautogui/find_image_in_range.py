import pyautogui

#default is to find image on screen this can be slow. 
pyautogui.locateOnScreen('someButton.png') 

#only scan from 0,0 to 300,400
pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))

