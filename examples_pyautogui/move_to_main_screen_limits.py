import pyautogui
import sys
w,h=pyautogui.size()  # current screen resolution width and height
xw=w-3 
yh=h-3

print("pyautogui max limit  x:" + str(w) + ",y:" + str(h) )

x,y = pyautogui.position()
print("Is our current mouse location on the main screen ?")
result=pyautogui.onScreen(xw,yh)  # True if x & y are within the screen
if result == True:
  print('current mouse location at x:' + str(xw) + ',y:' + str(yh) + " is on the main screen.")
else:
  print('current mouse location at x:' + str(xw) + ',y:' + str(yh) + " is not on the main screen exiting.")
  sys.exit()

try: 
  print("moving pointer to top of main screen.")
  pyautogui.moveTo(3,4,duration=3) #pygui doesn't like going to 0,0
  pyautogui.moveRel(+100,+100, duration=3)
except: 
  print("we encountered an unknown error.")

print("moving pointer to max_x or far left top corner of main screen.")
pyautogui.moveTo(xw,yh, duration=2) 
pyautogui.moveRel(-10,-10, duration=3)

print("moving pointer to max_y or far left bottom corner of main screen.")
pyautogui.moveTo(xw,yh,duration=1)