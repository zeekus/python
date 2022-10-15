import cv2 as cv
import numpy as np
import os, re, json, subprocess, pyautogui 
from PIL import ImageGrab
from time import time
#results: 26 - 40FPS on Linux on laptop
#import pydirectinput #ref uses assembly references for keyboard and mousemovements.
#import mss #seems to be faster with multi-platform support # https://github.com/BoboTiG/python-mss
#ref https://www.youtube.com/watch?v=WymCpVUPWQ4
#ref https://pypi.org/project/PyDirectInput/

#todo determine what type of action to perform based on the buttons provided
#look for cloaking device, look for mwd 


def set_focus_to_game():
   #get list of windows on the Linux desktop
   #wmctrl -lG | awk -F" " {'print $5,$6,$8,$9,$10'}
   if os.path.isfile("/usr/bin/wmctrl") == True :
     output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
     for line in output.stdout:
       parsed_line=(line.decode('utf-8').rstrip())
       if re.search("EVE -", parsed_line):
         window_title=re.sub(r'.*EV','EV',parsed_line)
         print (window_title)
         out=subprocess.Popen(('wmctrl','-a',window_title)) #change the screen focus
         return 0 #successful
     return 1 #failed

def  load_target_data_from_json(path,json_file,target_message):
  f=open(json_file)        #open file
  data = json.load(f)      #load json data into mem
  f.close                  #close file

  file_array=[]
  #loop through the json data
  for i in data:
    message=i['message']
    filename=i['filename']
    if i['message'] == target_message:
      #print("appending " + path + "/" + filename )
      file_array.append(path + filename)

  return file_array

def return_image_center(x,y,w,h):
    center_x = x + int(w/2)
    center_y= y + int(h/2)
    return(center_x,center_y)

def flatten_image(image):

   #convert image to numpy array 
   image=np.array(image)

   #covert RGB to BGR
   #screenshot=screenshot[:, :, ::-1].copy() #numpy color conversion
   image= cv.cvtColor(image, cv.COLOR_RGB2BGR) #opencv color conversion

   #drop alpha channel data from the image
   image = image[...,:3] #numpy slice - slows down things.

   #fix type errors
   #final convert https://github.com/opencv/opencv/issues/#14866#issuecomment-580207109
   image = np.ascontiguousarray(image)
   return image

def get_screenshot():
   screenshot = ImageGrab.grab() #full screen
   #screenshot = ImageGrab.grab(bbox=(0,0,300,300)) #specific screen region
 
   screenshot=flatten_image(screenshot)

   return screenshot

    
# Change to the working director to the folder if needed.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time=time()
focus_error=set_focus_to_game()

while(True):

   #press 'q' with the output window focused to quit
   #waits 1 ms every loop to process key presses.
   if cv.waitKey(1) == ord('q') or focus_error==1:
     cv.destroyAllWindows() #clean up all the open cv windows we have
     if focus_error ==1: 
       print ("Error Game window not found.")
     else:
       print ("exiting with no errors.")
     break

   screenshot=get_screenshot()
   #cv.imshow('Computer Vision', screenshot )
   align_button=None
   warpto_button=None
   warp_button_img="/home/ted/Documents/git/python/open_cv/buttons/__warpto0.png"
   align_button_img="/home/ted/Documents/git/python/open_cv/buttons/__align.png"
   align_button=pyautogui.locate(align_button_img,screenshot,confidence=0.85)
   warpto_button=pyautogui.locate(warp_button_img,screenshot,confidence=0.85)
   if align_button != None:
     print("we see the align button")
     print("align_button is " + str(align_button))
   if warpto_button != None:
     print("we see the warp to button")
     print("warp_to is " + str(warpto_button))
     

   if warpto_button != None and align_button != None:
      warp_to= cv.imread(warp_button_img,cv.IMREAD_UNCHANGED)
      # Save the dimensions of the needle image
      w = warp_to.shape[0]
      h = warp_to.shape[1]
      x,y=return_image_center(warpto_button[0],warpto_button[1],w,h)
      pyautogui.moveTo(x,y,2)
      pyautogui.click()
      break

   print('FPS {}'.format(1/ (time() - loop_time))) #get FPS required 
   loop_time=time()



print('Done.')
