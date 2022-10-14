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

def get_screenshot():
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
   align_button=pyautogui.locate("/home/ted/Documents/git/python/open_cv/buttons/__align.png",screenshot,confidence=0.8)
   #align_button=pyautogui.locate("/home/ted/Documents/git/python/open_cv/buttons/__align.png",screenshot) #no cv
   if align_button != None:
     print("we see the align button")
     x=align_button[0]
     y=align_button[1]
     w=align_button[2]
     h=align_button[3]
     center=[int(x+(w/2)),int(y+(h/2))] #find center 
     print(center)
     pyautogui.moveTo(center[0],center[1],2)
     exit()
     #Box(left=1145, top=414, width=30, height=21)
     #need a find center method to find center.

  #  if ( screenshot != None):
  #    w,h=screenshot.size
  #    print("w:%s,h:%s" % ( w,h))
   print('FPS {}'.format(1/ (time() - loop_time))) #get FPS required 
   loop_time=time()



print('Done.')