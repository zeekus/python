#!/usr/bin/python3
#filename: multipurpose_warper.py
#uses pyautogui to control a space ship in warp.
#four types of warps "mwd" - mwd trick, "c" - cloaking, 'noa' - noalign, and "n" - normal 

import time
import os
import pyautogui
import json
import sys
import random
import re
import subprocess
from rotatecamera import RotateCamera #import rotate camera class


def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error

def  load_target_data_from_json(path,json_file,target_message):
  f=open(json_file)        #open file
  data = json.load(f)      #load json data into mem
  f.close                  #close file

  #print(f"debug: source json file is #{json_file}")

  file_array=[]
  #loop through the json data
  for i in data:
    message=i['message']
    filename=i['filename']
    if i['message'] == target_message:
      # print("load_target_data_from_json - appending " + path + filename )
      file_array.append(path + filename)

  return file_array

def return_image_center_from_box(box):
   #print("Debug: return_image_center_from_box -" + str(box))
   if box!=None: 
     x,y,w,h=box
     return x + int(w/2), y+ int(h/2)
   else:
     print("Error: Box variable not found - fatal error exiting.")
     sys.exit()

def find_target_image_on_screen(message,top=None,bottom=None):
  if top==None or bottom==None:
    return pyautogui.locateOnScreen(message, confidence=0.81)
  else:
    return pyautogui.locateOnScreen(message, region=(top[0],top[1], bottom[0], bottom[1]),confidence=0.81)

def find_one_image_from_many_files(my_array,top=None,bottom=None):
    #print("find_one_image_from_many_files")
    for image in my_array:
      result=find_target_image_on_screen(image,top,bottom)
      if result != None:
         return result,image #location result and imagefile
    return None,""

def randomize_xy(x,y):
   return x+random.randrange(-2,2,1),y+random.randrange(-2,2,1)

def pymove(location):
   pyautogui.moveTo(location[0],location[1],2, pyautogui.easeOutQuad)    # start fast, end slow

def click_button(x,y,speed,description):
  match = re.search('button', description)
  if match:
    x,y=randomize_xy(x,y) #randomize click location 1-2 pixels each time
  pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
  print("Info: - click_button() - '" + description + "' button center at:" +  "x:" + str(x) + "y:" + str(y),end='');print_time()
  pyautogui.click(x,y)

def exit_if_docked(buttons_folder,button_json_file,mystart,jump_gates_traversed):
    undock_image_exists,dfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="undock button found")
    if undock_image_exists != None: #in station
       print("we appear docked. Exiting.")
       mins=((time.time()-mystart)/60)
       print("We appear to be docked. Exiting. run time: " + f'{mins:5.2f} ' + " minutes")
       print("jumps complete: " + str(jump_gates_traversed))
       sys.exit()
    else:
      return None

def search_for_image_return_location(path,data_file,target,top=None,bottom=None):
   result=None # default to none
   images=[]
   try: 
     images=load_target_data_from_json(path,data_file,target)
   except: 
     print(f"we failed to load #{target} from {path}{data_file}")
   result,imagefile=find_one_image_from_many_files(images,top,bottom)
   return result,imagefile

def click_jump(jump_button_center):
    time.sleep(.5)
    click_button(jump_button_center[0],jump_button_center[1],1,"clicking jump button") #click jump button

def cloak_sequence(align_button_center,cloak_button_center,jump_button_center):
    click_button(align_button_center[0],align_button_center[1],1,"clicking align button") #click align button
    time.sleep(1)
    click_button(cloak_button_center[0],cloak_button_center[1],1,"clicking cloak button") #click cloak button

def mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center):
    click_button(align_button_center[0],align_button_center[1],1,"clicking align button") #click align button
    time.sleep(1)
    click_button(cloak_button_center[0],cloak_button_center[1],1,"clicking cloak button") #click cloak button
    click_button(mwd_button_center[0],mwd_button_center[1],1,"clicking mwd button")#click mwd button
    time.sleep(4)
    click_button(cloak_button_center[0],cloak_button_center[1],1,"clicking cloak button") #click cloak button
    
def icon_button_action(path,data_file,target="yellow gate icon",top=-1,bottom=-1):
  button_center=""
  my_result=None # set yellow result as 0 
  print (f"Info: icon_button_action() - target is {target} - top is {top} and bottom is {bottom}")
  if top != -1 and bottom != -1:
    #limit defined
    my_result,myfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target=target,top=top,bottom=bottom)
  else:
    #search entire screen
    my_result,myfile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target=target)
  button_center=return_image_center_from_box(my_result) #locate center
  print(f"Info: {target} button center: {button_center}")
  click_button(x=button_center[0],y=button_center[1],speed=2,description=target)
  return my_result,button_center,myfile

def print_time():
  named_tuple = time.localtime() # get struct_time
  time_string = time.strftime(" Time: %m/%d/%Y, %H:%M:%S", named_tuple)
  print(str(time_string))

def rotate_camera_if_needed(w,h):
  nav_bar_too_bright=False
  # start_x = w-500 #500 pixels in from right edge of monitor 
  # start_y = 0     #top of screen 
  camera_rotations=0
  a=RotateCamera(w,h) #initialize class 

  nav_bar_too_bright=a.check_range_for_color_bleed()
  while nav_bar_too_bright is True:
    a.randomize_xy_drag()
    camera_rotations=camera_rotations+1
    nav_bar_too_bright=a.check_range_for_color_bleed()
    pyautogui.sleep(1)
  print(f'Info: rotate_camera_if_needed() - completed {camera_rotations} - camera rotations. ')

path=os.getcwd() #get current working directory 
buttons_folder=(path + "/buttons/") #button images
button_json_file =(buttons_folder + "buttons.json")  #description of button images
messages_folder=(path + "/messages/") #message images
message_json_file=(messages_folder + "messages.json") #description of message images
mystart=time.time()
jump_gates_traversed=0  
undock_image_exists = exit_if_docked(buttons_folder,button_json_file,mystart,jump_gates_traversed)

my_screensize=pyautogui.size()
w=my_screensize[0] #width  aka x
h=my_screensize[1] #height aka y
seq=[] # process

#define the type of warp to do 
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
if (len(sys.argv)-1) > 0:
  print("we have more than one argument.")
  if sys.argv[1]=="c":
    warp_type="cloaking"
    seq=["align","cloak","jump"]
  elif sys.argv[1]=="mwd":
    seq=["align","cloak","mwd on", "mwd off", "decloak", "jump"]
    warp_type="mwd"
  elif sys.argv[1]=="noa": #no alignS
    seq=["jump"]
    warp_type="noa"
  else:
    seq=["align","jump"]
    warp_type="normal"
else:
  print("we have less than one argument.")
  print("arguments are 'c' 'mwd' or '0'" )
  sys.exit()

print(warp_type)

focus_error=focus_window("VE -") #partial name open game window
if focus_error ==1:
  print(f"did not find game window error: {error}")
  sys.exit()

#click yellow icon 
yellow_result,yellow_button_center,yfile=icon_button_action(path=buttons_folder,data_file=button_json_file)#do we need anything here ? 

#Calibration: find center of all the buttons at the beginning of the run.
print("Info: Calibrations: finding locations for nav window items.")
align_button_found,align_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align button")
jump_button_found,jb_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="jump button")
ibutton_found,ib_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="ibutton")
mwd_button_found,mwd_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="mwd button")
cloak_button_found,cloak_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="cloak button")

print("Info: calibrating center on clickables ...",end=''); print_time()

#sanity checks 
#Find button centers 
if align_button_found is not None: 
  print("attempting to find " + str(align_file) + " center.")
  align_button_center=return_image_center_from_box(align_button_found)
else:
   print ("align_button_found is " + str(align_button_found))
if mwd_button_found is not None: 
  print("attempting to find mwd button center.")
  mwd_button_center=return_image_center_from_box(mwd_button_found)
else:
  print ("no mwd found")
if cloak_button_found is not None:
  print("attempting to find cloak button center.")
  cloak_button_center=return_image_center_from_box(cloak_button_found)
else:
  print ("no cloaking module found")
if jump_button_found is not None:
  print("attempting to find jump button center.")
  jump_button_center=return_image_center_from_box(jump_button_found)

if align_button_found is None or jump_button_found is None:
  print("Exiting with error state. Not able to find all of the required buttons.")
  sys.exit()

if warp_type=="mwd":
  if mwd_button_found is None or cloak_button_center is None: 
    print("Exiting with error state. Not able to find all the button center points for mwd jumps.")
    sys.exit()
elif warp_type=="cloak":
  if cloak_button_found is None: 
    print("Exiting with error state. Not able to find all the buttons for a cloaking jump.")
    sys.exit()
else: 
  print(f"{warp_type} jump sequence enabled.")


#define range of nav menu
print("Info: align_button:" + str(align_button_found))
nav_menu_box_top=align_button_found[0]-10,align_button_found[1]-10
print("Info: ibutton:" + str(ibutton_found))
nav_menu_box_bottom=ibutton_found[0]+27,ibutton_found[1]+27
print(f"Info: moving to nav_menu_box_top at {nav_menu_box_top}")
pymove(nav_menu_box_top)
print(f"Info: moving to nav_menu_box_bottom at {nav_menu_box_bottom}")
pymove(nav_menu_box_bottom)

#define yellow scan area
yellow_icon_top=nav_menu_box_top[0]+10,nav_menu_box_bottom[1]+50
pymove(yellow_icon_top)
yellow_icon_bottom=nav_menu_box_bottom[0],nav_menu_box_bottom[1]+700
pymove(yellow_icon_bottom)

print("Info: Button calibration complete...",end=''); print_time()

print("Info: rescanning for the yellow icon.")
#rescan for the yellow result in the limited area
yellow_result,yellow_button_center,yfile=icon_button_action(path=buttons_folder,data_file=button_json_file,target="yellow gate icon",top=yellow_icon_top,bottom=yellow_icon_bottom)

#############
##MAIN LOOP
#############

while undock_image_exists == None:

  rotate_camera_if_needed(w,h)
  
  #we need to verify the align button is always visable. 
  align_button_found_tmp,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align overview",top=nav_menu_box_top,bottom=nav_menu_box_bottom)
  if align_button_found_tmp is not None:
    align_button_found = align_button_found_tmp
  else:
    print("warning: unable to find the temp align button.")
    no_object_selected,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="no object selected",top=nav_menu_box_top,bottom=nav_menu_box_bottom)
    if no_object_selected is not None or align_button_found_tmp is None:
      align_button_found=None # reset align button found to force a rescan
      print("Info: no object selected icon detected. Attempting to find yellow icon. To get the nav bar back online.")
    
  if align_button_found==None: 
    align_button_scan_count=0 #counter 
    yellow_result=None #reset yellow_result to force a rescan 
    yellow_scan_count=0
    while yellow_result==None:
      yellow_result,yellow_button_center,yfile=icon_button_action(path=buttons_folder,data_file=button_json_file,target="yellow gate icon",top=yellow_icon_top,bottom=yellow_icon_bottom)
      yellow_scan_count=yellow_scan_count+1
      print(str(yellow_scan_count) + "yellow results:" + str(yellow_result) + "," + str(yfile))
      time.sleep(1) #sleep for 2 seconds
      if yellow_scan_count > 10:
        print("Error: not finding yellow icon - exiting.")
        sys.exit()
    
    while yellow_result != None and align_button_found == None:
      align_button_found,afile=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="align_overview",top=nav_menu_box_top,bottom=nav_menu_box_bottom)
      align_button_scan_count=align_button_scan_count+1
      if align_button_scan_count> 5:
        print("Error: align scan failure: exiting.")
        sys.exit()
  else: 
    print("Info: align_button_found:" + str(align_button_found))

  #click on jump button when align button is visible.     
  if align_button_found is not None:
    jump_sequence_start=time.time() #mwd jump sequence starts

    #press jump button if align button is on screen
    if align_button_found is not None:
      if warp_type=="mwd":
        mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center)
      elif warp_type=="cloaking":
        cloak_sequence(align_button_center,cloak_button_center,jump_button_center)
      else: #regular jump sequence 
        if warp_type!="noa":
          click_button(align_button_center[0],align_button_center[1],1,"clicking align button") #click align button
      #time.sleep(1)
      click_jump(jump_button_center)

      print("Info: verifying we are in warp.")
      #waiting for warp message to appear on the screen
      warp_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="warping")
      warp_wait=0
      while warp_message_found is None: 
       pyautogui.sleep(1)
       warp_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="warping")
       warp_wait=warp_wait+1
       if warp_wait == 10:
         print(f"Warning: Warping failed 10 times. Hitting jump again. We need a check here to verify.")
         click_jump(jump_button_center) 
       if warp_message_found is not None: 
         print(f"Info: Warping verfied.")
          
      #waiting for jump message to appear on the screen
      jump_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
                   
      while jump_message_found is None :
        print ('.', end='', flush=True)

        jump_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
        jump_seq_runtime=round(time.time()-jump_sequence_start,0)
        if ( jump_seq_runtime > 55 and jump_seq_runtime % 10):
          print ('w', end='', flush=True)
          dock_image_found=exit_if_docked(buttons_folder,button_json_file,mystart,jump_gates_traversed) #look for docking image
          approach_button_found,approach_file=search_for_image_return_location(path=buttons_folder,data_file=button_json_file,target="approach button")
          if approach_button_found is not None and jump_message_found is None: 
            print(f"\nInfo: we appear hung up near a gate. {round(time.time()-jump_sequence_start,0)}") #ship ocassional
            click_jump(jump_button_center)
            while jump_message_found is None:
              jump_message_found,m_file=search_for_image_return_location(path=messages_folder,data_file=message_json_file,target="jumping")
              print ('*', end='', flush=True)
      
      if jump_message_found is not None:
        jump_gates_traversed=jump_gates_traversed+1
        jump_seq_runtime=((time.time()-jump_sequence_start)) 
        jump_info=(f"Info: {jump_gates_traversed}: Jumping Sequence completed. run time: {round(jump_seq_runtime)} - ")
        print( "\n" + jump_info, end=''); print_time()
        time.sleep(7)
