import time
import pyautogui
import os
import json

def  determine_target_files(json_file,target_message):
  f=open(json_file)        #open file
  data = json.load(f)      #load json data into mem
  f.close                  #close file

  file_array=[]

  #loop thorough the json data
  for i in data:
    message=i['message']
    filename=i['filename']
    if i['message'] == target_message:
      print("appending " + filename ) 
      file_array.append(filename)

  return file_array


path=os.getcwd()
json_file=(path + "/buttons/buttons.json")
target_files=[]
target_message=('yellow gate icon')
target_files=determine_target_files(json_file,target_message)

time.sleep(5)

for target_file in target_files:
  target_file =(path + "/buttons/" + target_file)
  p=pyautogui.locateOnScreen(target_file,region=(3481,212, 3498,614),confidence=0.9)
  if p != None:
     print(target_message + " at location :" + str(p[0]) + "," + str(p[1]) )
     print("moving mouse to:" +  str(p))
     pyautogui.moveTo(p[0],p[1],2, pyautogui.easeOutQuad)    # start fast, end slow
     print("clicking mouse at:" +  str(p))
     pyautogui.click(x=p[0], y=p[1])

     break



