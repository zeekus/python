#!/usr/bin/python3
#filename: multipurpose_warper.py
#uses pyautogui to control a space ship in warp.
#four types of warps "mwd" - mwd trick, "c" - cloaking, 'noa' - noalign, and "n" - noa+ 

import time
import os
import pyautogui
import json
import sys
import random
import re
import subprocess
from rotatecamera import RotateCamera #import rotate camera class
from calibration import Calibration 
from findimage import FindImage


def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    #print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error

def randomize_xy(x,y):
   return x+random.randrange(-2,2,1),y+random.randrange(-2,2,1)

def pymove(location):
   pyautogui.moveTo(location[0],location[1],2, pyautogui.easeOutQuad)    # start fast, end slow

def click_button(x,y,speed,description):
  match = re.search('button', description)
  if match:
    x,y=randomize_xy(x,y) #randomize click location 1-2 pixels each time
  pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
  print("Info: - click_button() - '" + description + "' center at: (" +  "x: " + str(x) + ",y: " + str(y) + ")" )
  pyautogui.click(x,y)

def return_image_center_from_box(box,description="empty"):
   #print("Debug: return_image_center_from_box - " + description + ":" + str(box)) 
   if box!=None: 
     x,y,w,h=box
     return x + int(w/2), y+ int(h/2)
   else:
     print(f"Error: return_image_center_from_box - {description} - {str(box)} - Box variable not found - fatal error exiting.")
     sys.exit()

def exit_if_docked(button_json_file,mystart,jump_gates_traversed,top=None,bottom=None):
    #print(f"Debug: - exit_if_docked - json file: {button_json_file}")
    undock_exists,dfile=FindImage.search_for_image_and_return_location(button_json_file,"undock button found",top,bottom)
    if undock_exists != None: #in station
       print("we appear docked. Exiting.")
       total_runtime=runtime_seconds(mystart)
       print(f"Info: We appear to be docked. Exiting. Total Run time: {convert(total_runtime)}")
       print("End: jumps complete: " + str(jump_gates_traversed))
       sys.exit()
    else:
      return None

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
    
def icon_button_action(data_file,target="yellow gate icon",top=None,bottom=None):
  button_center=""
  my_result=None # set yellow result as 0 
  print (f"Info: icon_button_action() - target is {target} - top is {top} and bottom is {bottom}")
  # if top != -1 and bottom != -1: #x,y target area defined 
  my_result,myfile=FindImage.search_for_image_and_return_location(json_file=data_file,message=target,top=top,bottom=bottom)
  # else: #search entire screen
  #   my_result,myfile=FindImage.search_for_image_and_return_location(json_file=data_file,message=target)
  button_center=return_image_center_from_box(my_result,target) #locate center
  print(f"Info: {target} button center: {button_center}")
  click_button(x=button_center[0],y=button_center[1],speed=2,description=target)
  return my_result,button_center,myfile

# def print_time():
#   named_tuple = time.localtime() # get struct_time
#   time_string = time.strftime(" Time: %m/%d/%Y, %H:%M:%S", named_tuple)
#   print(str(time_string))

def runtime_seconds(mystart):
  return (round(time.time()-mystart)) #seconds

def convert(seconds):
   return time.strftime("%H:%M:%S", time.gmtime(seconds))

def rotate_camera_if_needed(w,h):
  nav_bar_too_bright=False
  camera_rotations=0
  a=RotateCamera(w,h) #initialize class 

  nav_bar_too_bright=a.check_range_for_color_bleed()
  while nav_bar_too_bright is True:
    a.randomize_xy_drag()
    camera_rotations=camera_rotations+1
    nav_bar_too_bright=a.check_range_for_color_bleed()
    pyautogui.sleep(1)
  print(f'Info: rotate_camera_if_needed() - completed {camera_rotations} - camera rotations. ')

def helpme():
   print("sys.argv recieved the wrong arguments.")
   print(f"help: '{sys.argv[0]} c' for 'cloaking', '{sys.argv[0]} mwd' for 'micro warp drive', '{sys.argv[0]} noa' for 'no aligns' , '{sys.argv[0]} noa+' for 'noa+ aligns'")
   sys.exit()

path=os.getcwd() #get current working directory 
button_json_file =(f"{path}/buttons/buttons.json")   #description of button images
message_json_file=(f"{path}/messages/messages.json") #description of message images
mystart=time.time()
jump_gates_traversed=0  
undock_exists = exit_if_docked(button_json_file,mystart,jump_gates_traversed)

#define the type of warp to do 
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
if (len(sys.argv)-1) > 0:
  print("we have more than one argument.")
  if sys.argv[1]=="c" or sys.argv[1]=="mwd" or sys.argv[1]=="noa" or sys.argv[1]=="noa+":
    warp_type=sys.argv[1]
  else:
    helpme()
else:
    help(me)

focus_error=focus_window("VE -") #partial name open game window
if focus_error ==1:
  print(f"did not find game window error: {error}")
  sys.exit()

print("Calibrating Screen using pyautogui")
w,h=pyautogui.size()
myval=Calibration(w,h) #sets up screen refernce points and return as myval

#check to make sure we have all the items selected before pressing buttons 
if warp_type=="c" or warp_type=="mwd": #scan cloak button
  cloak_bf,cloak_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="cloak button",top=myval.top_left,bottom=myval.bottom_right)
  cloak_button_center=return_image_center_from_box(cloak_bf,"cloak button")
else:
  cloak_bf=None
if warp_type=="mwd":
   mwd_button_found,mwd_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="mwd button",top=myval.top_left,bottom=myval.bottom_right)
   mwd_button_center=return_image_center_from_box(mwd_button_found,"mwd button")
else:
  mwd_button_found=None
print("Info: calibrating center on clickables ...",end='')

yellow_result,yellow_button_center,yfile=icon_button_action(data_file=button_json_file,top=myval.navbar_ltop,bottom=myval.bottom_right) #yellow gate icon if destination set
align_bf,align_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="align button",top=myval.navbar_ltop,bottom=myval.bottom_right) #align if yellow clicked
align_button_center=return_image_center_from_box(align_bf,"align button")
ibutton_found,ib_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="ibutton",top=myval.navbar_ltop,bottom=myval.bottom_right) #icon if yellow clicked
nav_bar_top=[ align_bf[0], align_bf[1] ] #define scan region start box for common buttons -  to speed up things 
nav_bar_bot=[ ibutton_found[0]+ibutton_found[2], ibutton_found[1]+ibutton_found[3] ] #define scan region end box
#define yellow scan area
yellow_icon_top=nav_bar_top[0],nav_bar_top[1]+50
yellow_icon_bottom=nav_bar_bot[0],nav_bar_bot[1]+700

#Calibration: find center of all the buttons at the beginning of the run.
print("Info: Calibrations: finding locations for nav window items.")
jump_bf,jb_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="jump button",top=nav_bar_top,bottom=nav_bar_bot) #jump button location
jump_button_center=return_image_center_from_box(jump_bf,"jump button")

#checking nav bar range
print("Info: align_button:" + str(align_bf))
print("Info: ibutton:" + str(ibutton_found))

debug_boxes=0
if debug_boxes==1:
  print(f"Debug: moving to nav_bar_top at {nav_bar_top}")
  pymove(nav_bar_top)
  print(f"Debug: moving to nav_bar_bot at {nav_bar_bot}")
  pymove(nav_bar_bot)
  print(f"Debug: moving to yellow_icon_top.")
  pymove(yellow_icon_top)
  print(f"Debug: moving to yellow_icon_bottom.")
  pymove(yellow_icon_bottom)
print("Info: Button calibration complete...")

print("Info: rescanning for the yellow icon.")
yellow_result,yellow_button_center,yfile=icon_button_action(data_file=button_json_file,target="yellow gate icon",top=yellow_icon_top,bottom=yellow_icon_bottom)

#############
##MAIN LOOP
#############

while undock_exists == None:

  rotate_camera_if_needed(w,h)
  
  #we need to verify the align button is always visable. 
  align_bf_tmp,align_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="align button",top=nav_bar_top,bottom=nav_bar_bot)
  if align_bf_tmp is not None:
    align_bf = align_bf_tmp
  else:
    print("Warning: unable to find the temp align button.")
    dock_image_found=exit_if_docked(button_json_file,mystart,jump_gates_traversed) #look for docking image exit if found
    align_bf,align_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="align button",top=nav_bar_top,bottom=nav_bar_bot)
    nos,afile=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="no object selected",top=nav_bar_top,bottom=nav_bar_bot)
    if nos is not None or align_bf_tmp is None:
      align_bf=None # reset align button found to force a rescan
      print("Info: no object selected icon detected. Attempting to find yellow icon. To get the nav bar back online.")
    
  if align_bf==None: 
    align_button_scan_count=0 #counter 
    yellow_result=None #reset yellow_result to force a rescan 
    yellow_scan_count=0
    while yellow_result==None:
      yellow_result,yellow_button_center,yfile=icon_button_action(data_file=button_json_file,target="yellow gate icon",top=yellow_icon_top,bottom=yellow_icon_bottom)
      yellow_scan_count=yellow_scan_count+1
      print(str(yellow_scan_count) + "yellow results:" + str(yellow_result) + "," + str(yfile))
      time.sleep(1) #sleep for 2 seconds
      if yellow_scan_count > 10:
        print("Error: not finding yellow icon - exiting.")
        sys.exit()
    
    while yellow_result != None and align_bf == None:
      align_bf,align_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="align button",top=nav_bar_top,bottom=nav_bar_bot)
      align_button_scan_count=align_button_scan_count+1
      if align_button_scan_count> 5:
        print("Error: align scan failure: exiting.")
        sys.exit()
  else: 
    print("Info: align_bf:" + str(align_bf))

  #click on jump button when align button is visible.     
  if align_bf is not None:
    jump_sequence_start=time.time() #mwd jump sequence starts

    #press jump button if align button is on screen
    if align_bf is not None:
      if warp_type=="mwd":
        mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center)
      elif warp_type=="c":
        cloak_sequence(align_button_center,cloak_button_center,jump_button_center)
      else: #regular jump sequence 
        if warp_type!="noa":
          click_button(align_button_center[0],align_button_center[1],1,"clicking align button") #click align button
          time.sleep(2)
      click_button(jump_button_center[0],jump_button_center[1],1,"clicking jump button") #click jump after all the different types of processes.

      print("Info: verifying we are in warp.")
      #waiting for warp message to appear on the screen
      warp_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="warping",top=myval.top_left,bottom=myval.bottom_right)
      warp_wait=0
      warp_start=time.time()
      while warp_mf is None: 
       warp_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="warping",top=myval.top_left,bottom=myval.bottom_right)
       warp_wait=warp_wait+1
       if warp_wait %10 == 0 and warp_mf is None:
         print(f"Warning: Warping failed 10 times. Hitting jump again. We need a check here to verify.")
         click_button(jump_button_center[0],jump_button_center[1],1,"clicking jump button") #click jump
       if warp_mf is not None: 
           print("Info: Warping: ", end="")
      jump_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="jumping",top=myval.top_left,bottom=myval.bottom_right)
      while warp_mf is not None and jump_mf is None:
        warp_time=runtime_seconds(warp_start)
        print ('*', end='', flush=True)
        warp_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="warping",top=myval.top_left,bottom=myval.bottom_right)
        jump_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="jumping",top=myval.top_left,bottom=myval.bottom_right)
      print(f"\nInfo: warp took {warp_time} seconds.")
      print(f"Info: Waiting for jump message.") #waiting for jump message to appear on the screen
      while jump_mf is None:
        jump_mf,m_file=FindImage.search_for_image_and_return_location(json_file=message_json_file,message="jumping",top=myval.top_left,bottom=myval.bottom_right)
        jump_seq_runtime=runtime_seconds(jump_sequence_start)
        print ('.', end='', flush=True)
        if ( jump_seq_runtime > 15 and jump_seq_runtime % 10):
          print ('w', end='', flush=True)
          dock_image_found=exit_if_docked(button_json_file,mystart,jump_gates_traversed) #look for docking image
          approach_bf,my_a_file=FindImage.search_for_image_and_return_location(json_file=button_json_file,message="approach button",top=nav_bar_top,bottom=nav_bar_bot)
          if approach_bf is not None and jump_mf is None: 
            print(f"\nInfo: we appear hung up near a gate. {convert(jump_seq_runtime)}")       #ship ocassional gets hung up 
            click_button(jump_button_center[0],jump_button_center[1],1,"clicking jump button")  #click jump and pray - need to revisit later. 
            jump_mf=1 #assume things are working
      
      if jump_mf is not None:
        jump_gates_traversed=jump_gates_traversed+1
        jump_seq_runtime=runtime_seconds(jump_sequence_start)
        total_runtime=runtime_seconds(mystart)
        print(f"Info: {jump_gates_traversed}: Jumping Sequence completed. local runtime: {convert(jump_seq_runtime)}. Total Run time: {convert(total_runtime)} ")
        #todo we should try and scan for verification of the session change
        time.sleep(7)
