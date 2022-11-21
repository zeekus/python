
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
  #loop thorough the json data
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
    for image in my_array:
      result=find_target_image_on_screen(image)
      if result != None:
         return result,image #location result and imagefile

def click_button(x,y,speed,description):
    #click button at location
    pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
    print("clicking " + description + " button at:" +  "x:" + str(x) + "y:" + str(y))
    pyautogui.click(x,y)

def exit_if_docked(buttons_folder,button_json_file,mystart):
    #print("checking for undock images.")
    undock_buttons=[]
    undock_buttons=load_target_data_from_json(buttons_folder,button_json_file,"undock button found")
    undock_image_exists,imagefile=find_one_image_from_many_files(undock_buttons)
    if undock_image_exists != None: #in station
       print("we appear docked. Exiting.")
       print("run time was " + str(time.time()-mystart) + " seconds")
       sys.exit()
    else:
      return None

def search_for_image_return_location(path,data_file,target):
   result=None # default to none
   images=[]
   images=load_target_data_from_json(path,data_file,target)
   result,imagefile=find_one_image_from_many_files(images)
   return result,imagefile

def search_for_image_return_center_location(imagefile):
   return center=locateCenterOnScreen(imagefile,confidence=0.9)

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
      yellow_destination_icon=[]
      yellow_destination_icon=load_target_data_from_json(buttons_folder,button_json_file,"yellow gate icon")
      yellow_result,imagefile=find_one_image_from_many_files(yellow_destination_icon)
      time.sleep(2) #sleep for 2 seconds

    #verify the align button is visible
    align_button_found=None
    align_button_found,imagefile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align_overview")
    print("align button check result is " + str(align_button_found))

    if yellow_result is not None and align_button_found is None:
      #click yellow icon to get overview to refresh
      print("clicking on yellow icon")
      center=search_for_image_return_center_location(imagefile)
      click_button(x=center[0],y=center[1],speed=1,description="yellow icon")
      #click_button(x=yellow_result[0],y=yellow_result[1],speed=2,description="yellow icon")
    end
    
    if align_button_found is not None

      #verify the align button is visible
      align_button_found=None
      align_button_found,imagefile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align_overview")
      print("align button check result is " + str(align_button_found))

      #press jump button if align button is on screen
      if align_button_found is not None:
        clickable_jump_icon=None
        clickable_jump_icon,imagefile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="jump button")
        
        if clickable_jump_icon is not None:
          #click jump button 
          click_button(x=clickable_jump_icon[0],y=clickable_jump_icon[1],speed=2,description="jump button")
            
          #wait until jumping message appears
          jump_message_found=None
          dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart)

          while jump_message_found is None and dock_image_found is None:
            jumping_messages=[]
            jumping_messages=load_target_data_from_json(messages_folder,message_json_file,"jumping")
            jump_message_found,imagefile=find_one_image_from_many_files(jumping_messages)
            dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart)
            time.sleep(.5)
          #if jump_message_found is not None:
          if jump_message_found is not None:
            print("Jumping Sequence detected.")
            time.sleep(5)
