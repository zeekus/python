import cv2 as cv
import numpy as np
import os
import pyautogui 
import pydirectinput #ref uses assembly references for keyboard and mousemovements.

# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

while(True):
   screenshot = pyautogui.screenshot()

   #convert pyautogui to opencv
   screenshot=np.array(screenshot)

   #covert RGB to BGR
   #screenshot=screenshot[:, :, ::-1].copy() #numpy color conversion
   screenshot= cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) #opencv color conversion

   cv.imshow('Computer Vision', screenshot )
   
   #press 'q' with the output window focused to quit
   #waits 1 ms every loop to process key presses.
   if cv.waitKey(1) == ord('q'):
     cv.destroyAllWindows() #clean up all the open cv windows we have
     break

print('Done.')