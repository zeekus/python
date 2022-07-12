
#!/usr/bin/python3
#filename: simple_warper.py
#uses pyautogui to control a space ship in warp. 

import time
import os
import pyautogui
import json
import sys

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
      file_array.append(path + "/" + filename)

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

def click_button(x,y,speed,description):
    #click button at location
    pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
    print("clicking " + description + " button at:" +  "x:" + str(x) + "y:" + str(y))
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
   #return pyautogui.locateOnScreen(message, confidence=0.85)
   return pyautogui.locateCenterOnScreen(imagefile,confidence=0.85)


path=os.getcwd() #get current working directory 
buttons_folder=(path + "/buttons/") #button images
button_json_file =(buttons_folder + "buttons.json")  #description of button images
messages_folder=(path + "/messages/") #message images
message_json_file=(messages_folder+ "messages.json") #description of message images
mystart=time.time()
undock_image_exists = exit_if_docked(buttons_folder,button_json_file,mystart)


while undock_image_exists == None:
    #find and click the yellow destination icon 
    yellow_result=None

    while yellow_result==None:
      mytime=time.time() #time
      print(str(mytime) + " checking for the yellow icon.")
      yellow_result,yfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="yellow gate icon")
      print ("yellow results:" + str(yellow_result),str(yfile))
      time.sleep(2) #sleep for 2 seconds

    #verify the align button is visible
    align_button_found,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align overview")
    print("align button check result is " + str(align_button_found))

    no_obj_found,no_o_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="no object selected")
    print("no object check result is " + str(no_obj_found))
    

    if (( yellow_result is not None and no_obj_found) or align_button_found is None):
      #click yellow icon to get overview to refresh
      print("clicking on yellow icon at " + yfile )
      center=search_for_image_return_center_location(yfile)
      print("center is " + str(center))
      #click_button(x=center[0],y=center[1],speed=1,description="yellow icon")
      click_button(x=yellow_result[0],y=yellow_result[1],speed=2,description="yellow icon")
      #check for align button 
      align_button_found,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align_overview")
      print("align button check result is " + str(align_button_found))
    
    if align_button_found is not None:

      #press jump button if align button is on screen
      if align_button_found is not None:
        clickable_jump_icon=None
        clickable_jump_icon,jfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="jump button")
        
        if clickable_jump_icon is not None:
          #click jump button 
          center=search_for_image_return_center_location(jfile)
          #click_button(x=clickable_jump_icon[0],y=clickable_jump_icon[1],speed=2,description="jump button")
          click_button(x=center[0],y=center[1],speed=1,description="jump button")
          jump_sequence_start=time.time()
          time.sleep(5)
          jump_message_found,jfile=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
            

          while jump_message_found is None:
            #print("in jump sequence.")
            jump_message_found,jfile=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
            if ( time.time()-jump_sequence_start > 60 ):
               dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart) #look for docking image
               print("Warning after " + str(time.time()-jump_sequence_start) + " seconds. We are still watitng for a jump message." )

          if jump_message_found is not None:
            print("Jumping Sequence detected.")
            time.sleep(5)
