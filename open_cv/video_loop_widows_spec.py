import cv2 as cv
import numpy as np
import os
from time import time
import pyautogui 
import pydirectinput #ref uses assembly references for keyboard and mousemovements.
#import mss #seems to be faster with multi-platform support # https://github.com/BoboTiG/python-mss
#ref https://www.youtube.com/watch?v=WymCpVUPWQ4
#ref https://pypi.org/project/PyDirectInput/
import win32gui, win32ui, win32con 
from gi.repository import Gdk, GdkPixbuf #gdk libraries

#windows api to grab screen 
def windows_screenshot():
   #setup screen limits
   w = 1920 # set this
   h = 1080 # set this
  
   #hwnd = win32gui.FindWindow(None, windowname) #window name 
   hwnd = None # no window name 
   wDC = win32gui.GetWindowDC(hwnd)
   dcObj=win32ui.CreateDCFromHandle(wDC)
   cDC=dcObj.CreateCompatibleDC()
   dataBitMap = win32ui.CreateBitmap()
   dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
   cDC.SelectObject(dataBitMap)
   cDC.BitBlt((0,0),(w, h),dcObj,(0,0), win32con.SRCCOPY)
   dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

   #save the screenshot - for testing
   #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp') 
   signedIntsArray= dataBitMap.GetBitmapBits(True) #get bitmap
   img = np.fromstring(signedIntsArray, dtype='uint8') #convert bitmap to a numpy array
   img.shape = (h,w,4) #coverts to our height/width

   # Free Resources
   dcObj.DeleteDC()
   cDC.DeleteDC()
   win32gui.ReleaseDC(hwnd, wDC)
   win32gui.DeleteObject(dataBitMap.GetHandle())

   #remove alpha channel data from the image
   img = img[...,:3] #numpy slice - slows down things.

   #fix type errors
   #final convert https://github.com/opencv/opencv/issues/#14866#issuecomment-580207109
   img = np.ascontiguousarray(img)

   return img


#gdk function to grab screen
def image_grab_gtk(window):
    left, top, right, bot = get_rect(window)
    w = right - left
    h = bot - top

    s = gtk.gdk.Pixbuf(
        gtk.gdk.COLORSPACE_RGB, False, 8, w, h)

    s.get_from_drawable(
        gtk.gdk.get_default_root_window(),
        gtk.gdk.colormap_get_system(),
        left, top, 0, 0, w, h )

    final = Image.frombuffer(
        "RGB",
        (w, h),
        s.get_pixels(),
        "raw",
        "RGB",
        s.get_rowstride(), 1)
    return final

def gdk_image_grab():
  w = Gdk.get_default_root_window()
  sz = w.get_geometry()[2:4]
  #print "The size of the window is %d x %d" % sz
  pb = Gdk.pixbuf_get_from_window(w, 0, 0, sz[0], sz[1])
  if (pb != None):
    pb.savev("screenshot.png","png", [], [])
    print ("Screenshot saved to screenshot.png.")
  else:
    print ("Unable to get the screenshot.")



# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time=time()

while(True):
   #screenshot = pyautogui.screenshot()
   screenshot = windows_screenshot() 

   #convert pyautogui to opencv
   screenshot=np.array(screenshot)

   #covert RGB to BGR
   #screenshot=screenshot[:, :, ::-1].copy() #numpy color conversion
   screenshot= cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) #opencv color conversion

   cv.imshow('Computer Vision', screenshot )

   print('FPS {}'.format(1/ (time() - loop_time))) #get FPS required 
   loop_time=time()

   #press 'q' with the output window focused to quit
   #waits 1 ms every loop to process key presses.
   if cv.waitKey(1) == ord('q'):
     cv.destroyAllWindows() #clean up all the open cv windows we have
     break

print('Done.')