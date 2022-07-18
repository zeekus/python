
#!/usr/bin/python3
#filename: simple_warper.py
#uses pyautogui to control a space ship in warp. 

import time
import os
import pyautogui
import json
import sys
import random
import re

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

def find_target_image_on_screen(message):
    return pyautogui.locateOnScreen(message, confidence=0.85)

def find_one_image_from_many_files(my_array):
    #print("find_one_image_from_many_files")
    for image in my_array:
      result=find_target_image_on_screen(image)
      if result != None:
         return result,image #location result and imagefile
    return None,""

def randomize_xy(x,y):
   xr=random.randrange(0,3,1)
   yr=random.randrange(0,3,1)
 
   #print(str(xr),str(yr))

   if yr == 2:
     y=y-1
   else:
    y=y+yr
   if xr == 2:
     x=x-xr
   else:
     x=x+xr

   return x,y

def click_button(x,y,speed,description):
 match = re.search('button', string)
 if match:
    print("click original" + str(x) +str(y) )
    x,y=randomize_xy(x,y) #randomize click location 1-2 pixels each time
    print("click modified" + str(x) +str(y) )
 pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
 print("clicking " + description + " button center at:" +  "x:" + str(x) + "y:" + str(y))
 pyautogui.click(x,y)

def exit_if_docked(buttons_folder,button_json_file,mystart):
    undock_image_exists,dfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="undock button found")
   
    if undock_image_exists != None: #in station
       print("we appear docked. Exiting.")
       print("We appear to be docked. Exiting. run time: " + str(time.time()-mystart) + " seconds")
       sys.exit()
    else:
      return None

def search_for_image_return_location(path,data_file,target):
   #nested function - not the best code
   result=None # default to none
   images=[]
   images=load_target_data_from_json(path,data_file,target)
   result,imagefile=find_one_image_from_many_files(images)
   return result,imagefile

def search_for_image_return_center_location(imagefile):
   print("attempting to find center in " + str(imagefile) )
   return pyautogui.locateCenterOnScreen(imagefile,confidence=0.85)

def mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center):
    print_time()
    click_button(align_button_center[0],align_button_center[1],1,"clicking align button") #click align button
    time.sleep(2); print_time()
    click_button(cloak_button_center[0],cloak_button_center[1],1,"clicking cloak button") #click cloak button
    click_button(mwd_button_center[0],mwd_button_center[1],1,"clicking mwd button")#click mwd button
    time.sleep(1);print_time()
    click_button(mwd_button_center[0],mwd_button_center[1],2,"clicking mwd button") #click mwd button
    time.sleep(4);print_time()
    click_button(cloak_button_center[0],cloak_button_center[1],1,"clicking cloak button") #click cloak button
    time.sleep(.5);print_time()
    click_button(jump_button_center[0],jump_button_center[1],1,"clicking jump button") #click jump button

def get_time():
  named_tuple = time.localtime() # get struct_time
  time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
  return time_string

def print_time():
    mytime=get_time
    print(mytime)
    


path=os.getcwd() #get current working directory 
buttons_folder=(path + "/buttons/") #button images
button_json_file =(buttons_folder + "buttons.json")  #description of button images
messages_folder=(path + "/messages/") #message images
message_json_file=(messages_folder + "messages.json") #description of message images
mystart=time.time()
undock_image_exists = exit_if_docked(buttons_folder,button_json_file,mystart)

#Calibration: find center of all the buttons at the beginning of the run.
print("calibrating buttons...")
align_button_found,align_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align button")
mwd_button_found,mwd_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="mwd button")
cloak_button_found,cloak_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="cloak button")
jump_button_found,jb_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="jump button")

print("calibrating buttons center points...")

if align_button_found is not None: 
  print("attempting to find " + str(align_file) + " center.")
  align_button_center=search_for_image_return_center_location(align_file)
else:
   print ("align_button_found is " + str(align_button_found))
if mwd_button_found is not None: 
  print("attempting to find mwd button center.")
  mwd_button_center=search_for_image_return_center_location(mwd_file)
else:
  print ("mwd_button_found is " + str(mwd_button_found))
if cloak_button_found is not None:
  print("attempting to find cloak button center.")
  cloak_button_center=search_for_image_return_center_location(cloak_file)
else:
  print ("cloak_button_found is " + str(cloak_button_found))
if jump_button_found is not None:
  print("attempting to find jump button center.")
  jump_button_center=search_for_image_return_center_location(jb_file)
else:
  print ("jump_button_found is " + str(jump_button_found))

if align_button_found is None or mwd_button_found is None or cloak_button_found is None or jump_button_found is None:
  print("Exiting with error state. Not able to find all of the buttons.")
  sys.exit()
elif align_button_center is None or mwd_button_center is None or cloak_button_center is None or jump_button_found is None: 
  print("Exiting with error state. Not able to find all the button center points.")
  sys.exit()

else:
  print("button calibration was successful.")


while undock_image_exists == None:
    #find and click the yellow destination icon 
    yellow_result=None

    while yellow_result==None:
      mytime=get_time()
      yellow_result,yfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="yellow gate icon")
      print(str(mytime) + ":yellow results:" + str(yellow_result) + "," + str(yfile))
      time.sleep(2) #sleep for 2 seconds

    #verify the align button is visible
    align_button_found,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align overview")
    print("align_button_found1:" + str(align_button_found))
    
    #click on the yellow icon when the align overview images are not visible
    if ( align_button_found is None):
      #click yellow icon to get overview to refresh
      print("clicking on yellow icon at " + yfile )
      click_button(x=yellow_result[0],y=yellow_result[1],speed=2,description="yellow icon")
      #check for align button 
      align_button_found,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align_overview")
      print("align_button_found2:" + str(align_button_found))

    #click on jump button when align button is visible.     
    if align_button_found is not None:
      jump_sequence_start=time.time() #mwd jump sequence starts

      #press jump button if align button is on screen
      if align_button_found is not None:
        mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center)
        jump_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
                   
        while jump_message_found is None:
          #print("in jump sequence.")
          jump_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
          if ( time.time()-jump_sequence_start > 45 ):
            dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart) #look for docking image
            print("Warning after " + str(time.time()-jump_sequence_start) + " seconds. We are still waiting for a jump message." )

        if jump_message_found is not None:
          print("Jumping Sequence detected.")
          time.sleep(5)
