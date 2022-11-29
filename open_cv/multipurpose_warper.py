#!/usr/bin/python3
#filename: multipurpose_warper.py
#uses pyautogui to control a space ship in warp.
#four types of warps "mwd" - mwd trick, "c" - cloaking, 'noa' - noalign, and "n" - noa+ 
#known issues: click on yellow gate ocassional gets a different icon - this may be having opencv confidence variables set too low. 
#no verification when we hit the align button - need something to verify this is working
#no verification when we press jump a second time.

#todo add in log monitor script. This program will not work in T space 
#the log monitor displays 'docking' and 'jumping' when it happens. Need to use as failsafe.

#Rare Bug condition. - pending. 
#on a rare occassion the game causes the script to hang upon a jump.
#it is possible the opencv logic is too slow and reading the game logs will fix this.
#It seems the ship, jumps and the navbar turns to 'Nothing Found' but the script doesn't have logic to deal with this.

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
from parsegamelog import ParseGameLog

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
   print(f"debug: moving to {location}")
   pyautogui.moveTo(location[0],location[1],2, pyautogui.easeOutQuad)    # start fast, end slow

def click_button(x,y,speed,description,debug=1):
  match = re.search('button', description)
  if match:
    x,y=randomize_xy(x,y) #randomize click location 1-2 pixels each time
  pyautogui.sleep(1)
  pyautogui.moveTo(x,y,speed, pyautogui.easeOutQuad)    # start fast, end slow
  print(description + "center at: (" +  "x: " + str(x) + ",y: " + str(y) + ")" )  

  x1,y1=pyautogui.position()
  if x1==x and y1==y: 
     pyautogui.click()
  else:
    print("Warning: mouse moved.")

def return_image_center_from_box(box,description="empty",debug=0):
   #print("Debug: return_image_center_from_box - " + description + ":" + str(box)) 
   if box!=None:
     print(f"debug: return_image_center_from_box: box:{box}") 
     x,y,w,h=box
     if debug > 0:
       print(f"Debug: return_image_center_from_box for {description} at x:{x},y:{y},w:{w},h:{h} x+1/2w: {x+int(w/2)} y+1/2h:{y+int(h/2)}")
     return x + int(w/2), y+ int(h/2)
   else:
     print(f"Error: return_image_center_from_box - {description} - {str(box)} - Box variable not found - fatal error exiting.")
     sys.exit()

def exit_if_docked(button_json_file,mystart,jump_gates_traversed,top=None,bottom=None):
    #print(f"Debug: - exit_if_docked - json file: {button_json_file}")
    undock_exists=FindImage.search_for_image_and_return_location(button_json_file,"undock button found",top,bottom,0.85)
    if undock_exists != None: #in station
       print("\nWe appear docked. Exiting.")
       total_runtime=runtime_seconds(mystart)
       print(f"Info: We appear to be docked. Exiting. Total Run time: {convert(total_runtime)}")
       print("End: jumps complete: " + str(jump_gates_traversed))
       sys.exit()


def cloak_sequence(align_button_center,cloak_button_center,jump_button_center,loop_runtime):
    #message=(f"Info: {(convert(runtime_seconds(loop_runtime))} "1. cloak_trick - clicking align button ")
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 1. cloak_trick - clicking align button ")
    click_button(align_button_center[0],align_button_center[1],1,message,myval.debug) #click align button
    pyautogui.sleep(.5)
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 2. cloak_trick - clicking cloaking button - activation ")
    click_button(cloak_button_center[0],cloak_button_center[1],.5,message,myval.debug) #click cloak button

def mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center,loop_runtime):
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 1. mwd_trick - clicking align button ")
    click_button(align_button_center[0],align_button_center[1],.1,message,myval.debug) #click align button
    pyautogui.sleep(.5)
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 2. mwd_trick - clicking cloak button - activation ")
    click_button(cloak_button_center[0],cloak_button_center[1],.1,message,myval.debug) #click cloak button
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 3. mwd_trick - clicking mwd button - deactivation ")
    click_button(mwd_button_center[0],mwd_button_center[1],.2,message,myval.debug)#click mwd button
    pyautogui.sleep(4)
    message=(f"Info: {convert(runtime_seconds(loop_runtime))} 4. mwd_trick - clicking cloak button - deactivation ")
    click_button(cloak_button_center[0],cloak_button_center[1],1,message,myval.debug) #click cloak button
    
# def print_time():
#   named_tuple = time.localtime() # get struct_time
#   time_string = time.strftime(" Time: %m/%d/%Y, %H:%M:%S", named_tuple)
#   print(str(time_string))

def runtime_seconds(mystart):
  return (round(time.time()-mystart)) #seconds

def convert(seconds):
   return time.strftime("%H:%M:%S", time.gmtime(seconds))

def rotate_camera_if_needed(w,h,debug,force,camera_rotations_in_loop):
  nav_bar_too_bright=False
  print(f"Info: rotate_camera_if_need - force rotation set to {force}")
  a=RotateCamera(w,h,debug,force) #initialize class 

  nav_bar_too_bright=a.check_range_for_color_bleed()
  while nav_bar_too_bright is True or force==1:
    a.randomize_xy_drag()
    camera_rotations_in_loop=camera_rotations_in_loop+1
    print(f"Info: rotate_camera_if_needed - Camera rotations {camera_rotations_in_loop}")
    nav_bar_too_bright=a.check_range_for_color_bleed()
    pyautogui.sleep(1)
  
  return camera_rotations_in_loop

def helpme():
   print("sys.argv recieved the wrong arguments.")
   print(f"help: '{sys.argv[0]} c' for 'cloaking', '{sys.argv[0]} mwd' for 'micro warp drive', '{sys.argv[0]} noa' for 'no aligns' , '{sys.argv[0]} noa+' for 'noa+ aligns'")
   sys.exit()


path=os.getcwd() #get current working directory 
button_json_file =(f"{path}/buttons/buttons.json")   #description of button images
message_json_file=(f"{path}/messages/messages.json") #description of message images
mystart=time.time()
jump_gates_traversed=0  

#read game logs 
parse=ParseGameLog()
myfilename=parse.get_newest_game_file('GameLogs')
print(f"Info: Log filename is '{myfilename}'")

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
    helpme()

focus_error=focus_window("VE -") #partial name open game window
if focus_error ==1:
  print(f"did not find game window error: {error}")
  sys.exit()

print("Calibrating Screen using pyautogui")
w,h=pyautogui.size()
myval=Calibration(w,h) #sets up screen refpoints and return as myval object
print(f"Debug value in Calibrations class is set to {myval.debug}")

#check to make sure we have all the items selected before pressing buttons 
if warp_type=="c" or warp_type=="mwd": #scan cloak button
  cloak_bf=FindImage.search_for_image_and_return_location(button_json_file,"cloak button",myval.top_left,myval.bottom_right,0.85)
  cloak_button_center=return_image_center_from_box(cloak_bf,"cloak button",myval.debug)
else:
  cloak_bf=None
if warp_type=="mwd":
   mwd_button_found=FindImage.search_for_image_and_return_location(button_json_file,"mwd button",myval.top_left,myval.bottom_right,0.85)
   mwd_button_center=return_image_center_from_box(mwd_button_found,"mwd button",myval.debug)
else:
  mwd_button_found=None
print("Info: calibrating center on clickables ...")
yellow_gate=None
yellow_gate=FindImage.search_for_image_and_return_location(button_json_file,"yellow gate icon",myval.navbar_ltop,myval.bottom_right,0.80)
# print(f"debug: yellow scan 1 got {yellow_gate}")
align_bf=None 
if align_bf==None:
  if yellow_gate !=None: 
    print(f"debug: yellow click at  {yellow_gate}")
    click_button(yellow_gate[0]+2,yellow_gate[1]+1,1,"Initial: yellow icon click")
    pyautogui.sleep(1)
    align_bf=FindImage.search_for_image_and_return_location(button_json_file,"align button",myval.navbar_ltop,myval.bottom_right,0.85) #align if yellow clicked
  else:
    print("Fatal error: unable to find yellow icon.")
    sys.exit()
ibutton_found=FindImage.search_for_image_and_return_location(button_json_file,"ibutton",myval.navbar_ltop,myval.bottom_right,0.85) #icon if yellow clicked

nav_bar_top=[ align_bf[0], align_bf[1] ] #define scan region start box for common buttons -  to speed up things 
nav_bar_top_0=[nav_bar_top[0],5] #larger box 
#print(str(ibutton_found))
#sys.exit()
x=ibutton_found[0]+ibutton_found[2]
y=ibutton_found[1]+ibutton_found[3]
nav_bar_bot=[x,y] #define scan region end box

align_bf=FindImage.search_for_image_and_return_location(button_json_file,"align button",nav_bar_top,nav_bar_bot) #align if yellow clicked
align_button_center=return_image_center_from_box(align_bf,"align button")

#Calibration: find center of all the buttons at the beginning of the run.
print("Info: Calibrations: finding locations for nav window items.")
jump_bf=FindImage.search_for_image_and_return_location(button_json_file,"jump button",nav_bar_top,nav_bar_bot,0.85) #jump button location
jump_button_center=return_image_center_from_box(jump_bf,"jump button",myval.debug)

#checking nav bar range
print("Info: left nav bar  - align_button:" + str(align_bf))
print("Info: right nav bar - ibutton:     " + str(ibutton_found))

print("Info: Button calibration complete...")

#############
##MAIN LOOP
#############
#myval.screen_center screen center random
##click_button(myval.screen_center[0]+random.randrange(-50,50,1),myval.screen_center[1]+random.randrange(-70,70,1),1,"random center",myval.debug)
logtime,message=parse.readfile_getlast(myfilename,"Jumping") #get last jumping message
message_top=None  #message top variable - top of message - speeds up scans of messages.
message_bot=None  #message bot variable - bottom of message 
while True:
  loop_runtime=time.time() #loop run time
  camera_rotations_in_loop=0
  camera_rotations_in_loop=rotate_camera_if_needed(w,h,myval.debug,0,camera_rotations_in_loop)
   
  #we need to verify the align button is always visable.
  ibutton_found=FindImage.search_for_image_and_return_location(button_json_file,"ibutton",myval.navbar_ltop,nav_bar_bot,0.85)
  align_bf_tmp=FindImage.search_for_image_and_return_location(button_json_file,"align button",nav_bar_top,nav_bar_bot,0.85)
  no_obj_selected=FindImage.search_for_image_and_return_location(button_json_file,"no object selected",nav_bar_top_0,nav_bar_bot,0.85) # wider box
  if align_bf_tmp is not None and ibutton_found is not None and no_obj_selected == None:
    align_bf = align_bf_tmp #good 
  else:
    print("Warning: no align button, ibutton. Rescanning yellow:")
    dock_image_found=exit_if_docked(button_json_file,mystart,jump_gates_traversed) #look for docking image exit if found
    yellow_gate=FindImage.search_for_image_and_return_location(button_json_file,"yellow gate icon",nav_bar_top,myval.bottom_right,0.85)
    pyautogui.sleep(1)
    pyautogui.moveTo(myval.navbar_ltop[0],myval.navbar_ltop[1],1, pyautogui.easeOutQuad)
    yellow_dock=FindImage.search_for_image_and_return_location(button_json_file,"yellow docking icon",nav_bar_top,myval.bottom_right,0.85)
    if yellow_gate == None and yellow_dock == None:
      while yellow_gate == None and yellow_dock==None: # rescan until we find
        exit_if_docked(button_json_file,mystart,jump_gates_traversed) #look for docking image exit if found
        camera_rotations_in_loop=rotate_camera_if_needed(w,h,myval.debug,1,camera_rotations_in_loop) # can we force rotation
        print(f"c{camera_rotations_in_loop}",end='',flush=True)
        yellow_gate=FindImage.search_for_image_and_return_location(button_json_file,"yellow gate icon",nav_bar_top,myval.bottom_right,0.85)
        pyautogui.sleep(1)
        pyautogui.moveTo(myval.navbar_ltop[0],myval.navbar_ltop[1],1, pyautogui.easeOutQuad) #move mouse off screen work around to prevent bug 
        if yellow_gate == None:
          yellow_dock=FindImage.search_for_image_and_return_location(button_json_file,"yellow docking icon",nav_bar_top,myval.bottom_right,0.80)
        
    if yellow_dock != None:
      click_button(yellow_dock[0]+1,yellow_dock[1]+1,1,"Info: clicking dock icon",myval.debug)
    else:
      click_button(yellow_gate[0]+2,yellow_gate[1]+2,1,"Info: clicking yellow icon",myval.debug)
    ibutton_found=FindImage.search_for_image_and_return_location(button_json_file,"ibutton",myval.navbar_ltop,nav_bar_bot,0.85)
    align_bf_tmp=FindImage.search_for_image_and_return_location(button_json_file,"align button",nav_bar_top,nav_bar_bot,0.85)
 
    if ibutton_found is None and align_bf_tmp is None and yellow_gate is not None: 
      align_bf_tmp=FindImage.search_for_image_and_return_location(button_json_file,"align button",nav_bar_top,nav_bar_bot,0.85)
      align_bf = align_bf_tmp if align_bf_tmp != None else None

  print("Debug: align_bf:" + str(align_bf_tmp)) if myval.debug>0 else None

  #click on jump button when align button is visible.     
  if align_bf_tmp is not None:
    jump_sequence_start=time.time() #mwd jump sequence starts
    ###################################################
    #press jump button or preforming specified alterations if align button is on screen
    ###################################################
    if align_bf is not None:
      if warp_type=="mwd":
        mwd_trick_sequence(align_button_center,mwd_button_center,cloak_button_center,jump_button_center,loop_runtime)
      elif warp_type=="c":
        cloak_sequence(align_button_center,cloak_button_center,jump_button_center,loop_runtime)
      else: #regular jump sequence 
        if warp_type!="noa":
          message=(f"Info: {convert(runtime_seconds(loop_runtime))} clicking align button")
          click_button(align_button_center[0],align_button_center[1],1,message,myval.debug) #click align button
          time.sleep(2)
      message=(f"Info: {convert(runtime_seconds(loop_runtime))} clicking jump button")
      click_button(jump_button_center[0],jump_button_center[1],1, message,myval.debug) #click jump after all the different types of processes.
      print(f"Info: {convert(runtime_seconds(loop_runtime))} waiting for warp message:",end='',flush=True)

      ####################################################
      #waiting for warp message to appear on the screen  - need logic determine if this failed. 
      ####################################################
      warp_mf=None
      jump_mf=None
      warp_wait=0
      wait_count=0
      warp_start=time.time()
      while warp_mf is None and jump_mf==None: 
       warp_wait=round(time.time()-warp_start)
       if message_bot==None or message_top ==None: #can be buggy if scan area is too bright. - work round put blue ball on top of screen
        warp_mf=FindImage.search_for_image_and_return_location(message_json_file,"warping",myval.top_left,myval.bottom_right,0.81)
        jump_mf=FindImage.search_for_image_and_return_location(message_json_file,"jumping",myval.top_left,myval.bottom_right,0.81)
       else: 
        warp_mf=FindImage.search_for_image_and_return_location(message_json_file,"warping",message_top,message_bot,0.86)
        jump_mf=FindImage.search_for_image_and_return_location(message_json_file,"jumping",message_top,message_bot,0.86)
       print(".",end="",flush=True)
       if warp_wait % 30 == 0 and warp_mf is None and runtime_seconds(warp_start) > 30:
        print(f"\nWarning: {convert(runtime_seconds(loop_runtime))} Warping failed for {warp_wait} seconds. Hitting jump again. We need a check here to verify.")
        exit_if_docked(button_json_file,mystart,jump_gates_traversed)
        message=(f"Info: {convert(runtime_seconds(loop_runtime))} clicking jump button - after wait timeout.")
        click_button(jump_button_center[0],jump_button_center[1],1,message,myval.debug) #click jump and pray
      

      ##########################################
      #warp message detected on screen waiting for it to disappear
      ##########################################
      print(f"\nInfo: {convert(runtime_seconds(loop_runtime))} Warping: ", end="")
      while warp_mf is not None: 
        x,y,w2,h2=warp_mf #four fields come back x,y and image width,height - but we used w,h up above
        message_top=[x,y]
        message_bot=[x+w2,y+h2]
        warp_mf=FindImage.search_for_image_and_return_location(message_json_file,"warping",message_top,message_bot,0.85)
        jump_mf=FindImage.search_for_image_and_return_location(message_json_file,"jumping",message_top,message_bot,0.85)
        logtime_w,message_w=parse.readfile_getlast(myfilename,"Jumping") #get last jumping line
        print ('*', end='', flush=True)
      print("")

      warp_time=runtime_seconds(warp_start)
      print(f"Info: {convert(runtime_seconds(loop_runtime))} warp completed.")  
      
      ################################################
      #jump message detected on screen or in log
      ################################################
      jump_wstart=time.time()
   

      if jump_mf is not None or message!=message_w:
        jump_start=time.time()
        print(f"Info: {convert(runtime_seconds(loop_runtime))} Jump message detected.") #waiting for jump message to appear on the screen
      else:
        #waiting for jump message.
        print(f"Info: {convert(runtime_seconds(loop_runtime))} Waiting for jumping/docking message:", end='') #waiting for jump message to appear on the screen
        jwait_count=0
        approach_bf=None #approach button 
        logtime_j,message_j=parse.readfile_getlast(myfilename,"Jumping") #get last jumping line
        while jump_mf is None or message_j == message:
          game_style_time=time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime())
          logtime_j,message_j=parse.readfile_getlast(myfilename,"Jumping") #get last jumping line
          jump_mf=FindImage.search_for_image_and_return_location(message_json_file,"Jumping",message_top,message_bot,0.85)
          jwait_count=jwait_count+1
          jump_message_wait=runtime_seconds(jump_wstart)
          print ('w', end='', flush=True)
          if ( jump_message_wait> 15 and jwait_count % 10): 
            exit_if_docked(button_json_file,mystart,jump_gates_traversed) #look for docking image
            approach_bf=FindImage.search_for_image_and_return_location(button_json_file,"approach button",nav_bar_top,nav_bar_bot,0.82)
          if approach_bf != None: 
            print("Warning: {convert(runtime_seconds(loop_runtime))} We appear to be hung up on the gate.")
            message=(f"Info: {convert(runtime_seconds(loop_runtime))} clicking jump button - hung up on gate.")
            click_button(jump_button_center[0],jump_button_center[1],1,message) #click jump and pray
            jump_mf=True
        print("")
      jump_sequence_start=time.time()
      print(f"Info: {convert(runtime_seconds(loop_runtime))} Waiting for jump to complete:", end='') #waiting for jump message to leave screen 
      while warp_mf is None and jump_mf is not None:
        jump_mf=FindImage.search_for_image_and_return_location(message_json_file,"jumping",message_top,message_bot,0.85)
        print ('.', end='', flush=True)
      print("")
      jump_gates_traversed=jump_gates_traversed+1
      total_runtime=runtime_seconds(mystart)
      print(f"Info: {convert(runtime_seconds(loop_runtime))} {jump_gates_traversed}: Jumping Sequence completed. Total Run time: {convert(total_runtime)}")
      #todo we should try and scan for verification of the session change
      session_wait=10
      print(f"Waiting {session_wait} for session change: ", end='', flush=True)
      for x in range(session_wait):
         print(".",end='',flush=True)
         pyautogui.sleep(1)
      print("")#eol
      exit_if_docked(button_json_file,mystart,jump_gates_traversed)
