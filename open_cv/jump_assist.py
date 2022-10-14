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

def findClickPositions(needle_img_path, haystack_img, threshold=0.5, debug_mode=None):

    print("debug")
    print("needle_img_path:" + needle_img_path)
    print("debug_mode:" + debug_mode)
        
    # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
    #haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img_path,0)
    #needle_img = cv.cvtColor(needle_img, cv.COLOR_BGR2GRAY)#grayscale image
    # Save the dimensions of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    print(needle_w,needle_h)

    # There are 6 methods to choose from:
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    #result = cv.matchTemplate(haystack_img,needle_img,method)
    result = cv.matchTemplate(needle_img,haystack_img,method)
    if result == None:
       print("image not found.")
       exit()
    else:
       print("result is " + str(result)) 

    # Get the all the positions from the match result that exceed our threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    #print(locations)

    # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
    # locations by using groupRectangles().
    # First we need to create the list of [x, y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)
    # Apply group rectangles.
    # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
    # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
    # in the result. I've set eps to 0.5, which is:
    # "Relative difference between sides of the rectangles to merge them into a group."
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    #print(rectangles)

    points = []
    if len(rectangles):
        #print('Found needle.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:

            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                             lineType=line_type, thickness=2)
            elif debug_mode == 'points':
                # Draw the center point
                cv.drawMarker(haystack_img, (center_x, center_y), 
                              color=marker_color, markerType=marker_type, 
                              markerSize=40, thickness=2)

    if debug_mode:
        cv.imshow('Matches', haystack_img)
        #cv.waitKey()
        #cv.imwrite('result_click_point.jpg', haystack_img)

    return points

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
   warpto_button=None
   #align_button=pyautogui.locate("/home/ted/Documents/git/python/open_cv/buttons/__align.png",screenshot,confidence=0.8)
   align_button=findClickPositions(needle_img_path='/home/ted/Documents/git/python/open_cv/buttons/__align0.png',haystack_img=screenshot,threshold=0.5,debug_mode="rectangles")
   #warpto_button=findClickPositions("/home/ted/Documents/git/python/open_cv/buttons/__warpto.png",screenshot,0.5,'points')
   #align_button=pyautogui.locate("/home/ted/Documents/git/python/open_cv/buttons/__align.png",screenshot) #no cv
   if align_button != None:
     print("we see the align button")
     x=align_button[0]
     y=align_button[1]
    #  w=align_button[2]
    #  h=align_button[3]
    #  center=[int(x+(w/2)),int(y+(h/2))] #find center 
    #  print(center)
     pyautogui.moveTo(x,y,2)
     #pyautogui.moveTo(warpto_button,2)
     pyautogui.click()
     exit()
     #Box(left=1145, top=414, width=30, height=21)
     #need a find center method to find center.

  #  if ( screenshot != None):
  #    w,h=screenshot.size
  #    print("w:%s,h:%s" % ( w,h))
   print('FPS {}'.format(1/ (time() - loop_time))) #get FPS required 
   loop_time=time()



print('Done.')