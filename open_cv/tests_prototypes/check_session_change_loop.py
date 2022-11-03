#!/usr/bin/python3
#filename: check_session_change.py
#descrption: with too small of a data set. There are many false positives. This demonstrates the problem.
#this is a prototype 

import json,os,time,pyautogui,subprocess

def  loop_through_messages(file):
  f=open(file)        #open file
  data = json.load(f) #load json data into mem
  f.close             #close file

  #loop thorough the data
  for i in data:
    message=i['message']
    filename=i['filename']
    #print(i['message'] + "," + i['filename'])
    print(filename + ":" + message)
    path=os.getcwd()
    full_path_file=(path + "/session/" + filename)
    print(full_path_file)
    image=find_target_image_on_screen(full_path_file)
    if image == 1:
      computer_speak(message)
      

def find_target_image_on_screen(myfile):
  #using opencv find the image target on the screen
  now=later=time.time()
  print("myfile for the image target is " + myfile ) 
  image_target=pyautogui.locateOnScreen(myfile, confidence=0.9) #needs python-opencv2 returns object
  now_after_run=time.time()
  print ("runtime1 xy: " + str(now_after_run-now))
  if image_target != None: 
    return 1 #found
  else:
    return 0 #not found

def get_image_center_cords(myfile):  
  image_exists=find_target_image_on_screen(myfile)

  if image_exists == 1: 
    now=later=time.time()
    x,y=pyautogui.locateCenterOnScreen(myfile, confidence=0.9) #needs python-opencv2 object can't be NONE for this to run
    now_after_run2=time.time()
    print ("runtime2 xy: " + str(now_after_run2-now))
    print ("image target center on screen at " + str((x,y)) )
    # pyautogui.moveTo(image_target)
    # pyautogui.moveTo(x,y) #center of image 
    return x,y
  else:
    print ("image target not found on screen.")
    return 0,0

def computer_speak(message):
  if os.path.exists("/usr/bin/festival"):
    mytalk=("festival --tts")
    subprocess.call("echo " + message + "|" + mytalk, shell=True)
  elif os.path.exists("/usr/bin/espeak"):
    mytalk=("/usr/bin/espeak")
    subprocess.call("echo " + message + "|" + mytalk, shell=True)
  else:
    print("sorry this program needs either espeake or festival to talk.")
    sys.exit(1)

path=os.getcwd()
message_json=(path + "/session/session.json")

while True:
  loop_through_messages(message_json)
  time.sleep(1)

