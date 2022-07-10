

import time
import os
import pyautogui
import json

def  determine_target_files(path,json_file,target_message):
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

# def click(button):
#   time.sleep(5)
#   p=pyautogui.locateCenterOnScreen(button,confidence=0.9)
#   if p == None:
#     print ("no image found on screen")
#   else:
#     print("moving mouse to:" +  str(p))
#     pyautogui.moveTo(p[0],p[1],2, pyautogui.easeOutQuad)    # start fast, end slow
#     print("clicking mouse at:" +  str(p))
#     pyautogui.click(x=p[0], y=p[1])

def find_image_on_screen(message):
    return pyautogui.locateOnScreen(message, confidence=0.9)

# def click_on_jump_button(jumpicon,jump_message):
#   #click on jump button
#   click(jumpicon)
#   while jumping_message == None:
#     time.sleep(1)
#     #wait until Jumping messaging appears
#     jumping_message = find_image_on_screen(jump_message)

#   if jumping_message==None:
#       return 1 #fail
#   else: 
#       return 0 #success

def find_image_in_array(my_array):
    for image in my_array:
      result=find_image_on_screen(image)
      if result != None:
         return result

# def are_we_docked(button_json_file):
#   undock_button=[]
#   undock_button=determine_target_files(buttons_folder,button_json_file,"undock button found")
#   undock_image_exists=find_image_in_array(undock_button)
#   return undock_image_exists


path=os.getcwd()
buttons_folder=(path + "/buttons/")
button_json_file =(buttons_folder + "buttons.json")
messages_folder=(path + "/messages/")
message_json_file=(messages_folder+ "messages.json")

undock_image_exists = None #in space


while undock_image_exists == None:
    
    print("checking for undock image.")
    undock_buttons=[]
    undock_buttons=determine_target_files(buttons_folder,button_json_file,"undock button found")
    undock_image_exists=find_image_in_array(undock_buttons)

    #click yellow destination
    yellow_result=None

    while yellow_result==None:
      print("checking for the yellow icon.")
      yellow_destination_icon=[]
      yellow_destination_icon=determine_target_files(buttons_folder,button_json_file,"yellow gate icon")
      yellow_result=find_image_in_array(yellow_destination_icon)
      time.sleep(2) #sleep for 2 seconds

    if yellow_result is not None :
      #click yellow icon
      pyautogui.moveTo(yellow_result[0],yellow_result[1],2, pyautogui.easeOutQuad)    # start fast, end slow
      print("clicking yellow icon at:" +  str(yellow_result))
      pyautogui.click(x=yellow_result[0], y=yellow_result[1])

      #click on jump button
      align_button_found=None
      ready_to_align=[]
      ready_to_align=determine_target_files(buttons_folder,button_json_file,"aligning button configuration")
      align_button_found=find_image_in_array(ready_to_align)

      if ready_to_align is not None:
        clickable_jump_icon=None
        jump_buttons=[]
        jump_buttons=determine_target_files(buttons_folder,button_json_file,"jump button")
        clickable_jump_icon=find_image_in_array(jump_buttons)
        if clickable_jump_icon!=None:
          #click jump button 
          pyautogui.moveTo(clickable_jump_icon[0],clickable_jump_icon[1],2, pyautogui.easeOutQuad)    # start fast, end slow
          print("clicking jump button at:" +  str(clickable_jump_icon))
          pyautogui.click(x=clickable_jump_icon[0], y=clickable_jump_icon[1])
          
          #wait until jumping message appears
          jump_message_found=None

          while jump_message_found is None:
            jumping_messages=[]
            jumping_messages=determine_target_files(messages_folder,message_json_file,"jumping")
            jump_message_found=find_image_in_array(jumping_messages)
            time.sleep(.5)

          #if jump_message_found is not None:
          if jump_message_found is not None:
            print("Jumping Sequence detected.")
            time.sleep(5)


