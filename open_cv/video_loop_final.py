import cv2 as cv
import numpy as np
import os
from PIL import ImageGrab
from time import time
#results: 26 - 40FPS on Linux on laptop
#import pydirectinput #ref uses assembly references for keyboard and mousemovements.
#import mss #seems to be faster with multi-platform support # https://github.com/BoboTiG/python-mss
#ref https://www.youtube.com/watch?v=WymCpVUPWQ4
#ref https://pypi.org/project/PyDirectInput/

# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time=time()

while(True):
   screenshot = ImageGrab.grab() #full screen
   #screenshot = ImageGrab.grab(bbox=(0,0,300,300)) #specific screen region

   #convert pyautogui to opencv
   screenshot=np.array(screenshot)

   #covert RGB to BGR
   #screenshot=screenshot[:, :, ::-1].copy() #numpy color conversion
   screenshot= cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) #opencv color conversion

   #drop alpha channel data from the image
   screenshot = screenshot[...,:3] #numpy slice - slows down things.

   #fix type errors
   #final convert https://github.com/opencv/opencv/issues/#14866#issuecomment-580207109
   screenshot = np.ascontiguousarray(screenshot)
   cv.imshow('Computer Vision', screenshot )

   print('FPS {}'.format(1/ (time() - loop_time))) #get FPS required 
   loop_time=time()

   #press 'q' with the output window focused to quit
   #waits 1 ms every loop to process key presses.
   if cv.waitKey(1) == ord('q'):
     cv.destroyAllWindows() #clean up all the open cv windows we have
     break

print('Done.')