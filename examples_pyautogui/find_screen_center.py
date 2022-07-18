from turtle import screensize
import pyautogui

def return_screen_center():
   my_screensize=pyautogui.size()  # current screen resolution width and height
   print("main display has region of " + str(my_screensize))
   x=my_screensize[0]/2
   y=my_screensize[1]/2
   return x,y



x,y=return_screen_center()
print( 'Screen center is X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) )
pyautogui.moveTo(x,y,duration=2) 
pyautogui.moveRel(-1,+1, duration=3)