import cv2 as cv
import numpy as np
import os
import mss
from time import time
#results: 6- 400FPS on Linux on laptop. But slows down after running. - memory leak ? 
#import pydirectinput #ref uses assembly references for keyboard and mousemovements.
#import mss #seems to be faster with multi-platform support # https://github.com/BoboTiG/python-mss
#ref https://www.youtube.com/watch?v=WymCpVUPWQ4
#ref https://pypi.org/project/PyDirectInput/

# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time=time()

with mss.mss() as sct:
  
   monitor = {"top":40, "left":0, "width":800, "height":640 }

   while "Screen Capturing": 
      

      #raw pixels from screen, save as numpy array
      screenshot = np.array(sct.grab(monitor))

      #cv.imshow('opencv/normal image', screenshot ) #display the unmodified image
      cv.imshow("opencv/greyscale",cv.cvtColor(screenshot,cv.COLOR_BGRA2GRAY)) #grayscale image
      print('FPS {}'.format(60/ (time() - loop_time))) #get FPS required 
      last_time=time()
    

      #press 'q' with the output window focused to quit
      #waits 1 ms every loop to process key presses.
      if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows() #clean up all the open cv windows we have
        break

print('Done.')