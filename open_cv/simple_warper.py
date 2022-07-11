
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
         return result

def click_button(x,y,speed,description):
    #click button at location
    pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
    print("clicking " + description + " button at:" +  "x:" + str(x) + "y:" + str(y))
    pyautogui.click(x,y)

def exit_if_docked(buttons_folder,button_json_file,mystart):
    #print("checking for undock images.")
    undock_buttons=[]
    undock_buttons=load_target_data_from_json(buttons_folder,button_json_file,"undock button found")
    undock_image_exists=find_one_image_from_many_files(undock_buttons)
    if undock_image_exists != None: #in station
       print("we appear docked. Exiting.")
       print("run time was " + str(time.time()-mystart) + " seconds")
       sys.exit()
    else:
      return None

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
      print("checking for the yellow icon.")
      yellow_destination_icon=[]
      yellow_destination_icon=load_target_data_from_json(buttons_folder,button_json_file,"yellow gate icon")
      yellow_result=find_one_image_from_many_files(yellow_destination_icon)
      time.sleep(2) #sleep for 2 seconds

    if yellow_result is not None :
      #click yellow icon
      print("clicking on yellow icon")
      click_button(x=yellow_result[0],y=yellow_result[1],speed=2,description="yellow icon")

      #verify the align button is visible
      align_button_found=None
      ready_to_align=[]
      ready_to_align=load_target_data_from_json(buttons_folder,button_json_file,"align overview")
      align_button_found=find_one_image_from_many_files(ready_to_align)
      print("align button check result is " + str(align_button_found))

      #press jump button if align button is on screen
      if align_button_found is not None:
        clickable_jump_icon=None
        jump_buttons=[]
        jump_buttons=load_target_data_from_json(buttons_folder,button_json_file,"jump button")
        clickable_jump_icon=find_one_image_from_many_files(jump_buttons)
        if clickable_jump_icon is not None:
          #click jump button 
          click_button(x=clickable_jump_icon[0],y=clickable_jump_icon[1],speed=2,description="jump button")
            
          #wait until jumping message appears
          jump_message_found=None
          dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart)

          while jump_message_found is None and dock_image_found is None:
            jumping_messages=[]
            jumping_messages=load_target_data_from_json(messages_folder,message_json_file,"jumping")
            jump_message_found=find_one_image_from_many_files(jumping_messages)
            dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart)
            time.sleep(.5)
          #if jump_message_found is not None:
          if jump_message_found is not None:
            print("Jumping Sequence detected.")
            time.sleep(5)
