import pyautogui

# def right_side_of_screen_search(image):
#    my_screensize=pyautogui.size()  # current screen resolution width and height
#    x=my_screensize[0]/2
#    return pyautogui.locateOnScreen(image, region=(x,0, my_screensize[0], my_screensize[1]))

def left_side_of_screen_search(image):
   my_screensize=pyautogui.size()  # current screen resolution width and height
   width=my_screensize[0]/2
   height=my_screensize[1]
   #return pyautogui.locateOnScreen(image, region=(0,0, x, y))
   print( 'start X:' + str(0).rjust(4) + ', screen Y:' + str(0).rjust(4) )
   pyautogui.moveTo(1,1,duration=2) 
   print( 'end   X:' + str(width).rjust(4) + ', screen Y:' + str(height).rjust(4) )
   pyautogui.moveTo(int(width-1),int(height-1),duration=2)
   return pyautogui.locateOnScreen(image, region=(0,0, int(width), int(height)), confidence=0.85)

location_left=left_side_of_screen_search("__align.png")
print(str(location_left))

#default is to find image on screen this can be slow. 
#pyautogui.locateOnScreen('someButton.png') 

#only scan from 0,0 to 300,400
#pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))