import pyautogui
s=pyautogui.size()  # current screen resolution width and height
max_x=s[0]-1
max_y=s[1]-1
print("main display has region of " + str(s))
print("pyautogui max limit  x:" + str(max_x) + ",y:" + str(max_y) )

x,y = pyautogui.position()
#is 100,100 on the main screen ? 
result=pyautogui.onScreen(x, y)  # True if x & y are within the screen
if result == True:
  print('current mouse location at x:' + str(x) + ',y:' + str(y) + " is on the main screen.")
else:
  print('current mouse location at x:' + str(x) + ',y:' + str(y) + " is not on the main screen.")

print("moving pointer to top of main screen")
pyautogui.moveTo(1,1,duration=3) #pygui doesn't like going to 0,0
pyautogui.moveRel(+1,+1, duration=3)
print("moving pointer to max_x or far left top corner of main screen.")
pyautogui.moveTo(max_x,1,duration=2) 
pyautogui.moveRel(-1,+1, duration=3)
print("moving pointer to max_y or far left bottom corner of main screen.")
pyautogui.moveTo(max_x,max_y,duration=1)