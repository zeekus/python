import cv2 as cv
import numpy as np
import os

# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

while(True):
   screenshot = None
   cv.imshow('Computer Vision', screenshot )
   
   #press 'q' with the output window focused to quit
   #waits 1 ms every loop to process key presses.
   if cv.waitKey(1) == ord('q'):
     break
     
cv.destroyAllWindows()
print('Done.')
