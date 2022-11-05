import pyautogui 
import os
import json
import re

class FindImage:

   @staticmethod
   def find_target_image_on_screen(image,top=None,bottom=None):
     if top==None or bottom==None:
       return pyautogui.locateOnScreen(image, confidence=0.81)
     else:
       return pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=0.81)

   @staticmethod
   def return_image_location_from_array(my_array,top=None,bottom=None):
    result=None
    for image in my_array:
      result=FindImage.find_target_image_on_screen(image,top,bottom)
      if result != None:
         return result,image #location result and imagefile
    return None,""

   @staticmethod
   def  load_image_data_from_json(path,json_file,message):
     print(f"debug0 -target_message is {message}")
     print(f"debug1: load_image_data_from_json -  source json file is '{json_file}'")
     print(f"debug2: path is {path}")
     f=open(json_file)        #open file
     data = json.load(f)      #load json data into mem
     f.close                  #close file
     file_array=[]

     print(f"debug3: message is {message}")
                                                                                     
     if re.search('button',message) or re.search('yellow',message):
       filetype="buttons"
     else:
       filetype="messages"
                                                                                     
     for i in data:
      if re.search( message, i['message']):
        fullpath=(f"{os.getcwd()}/{filetype}/{i['filename']}")
        file_array.append(fullpath)
     return file_array

   @staticmethod
   def search_for_image_and_return_location(path,json_file,message,top=None,bottom=None):
     result=None # default to none
     images=[]
     print(f"debug: searching for a {message} button")
     images=FindImage.load_image_data_from_json(path,json_file,message)
     result,imagefile=FindImage.return_image_location_from_array(images,top,bottom)
     return result,imagefile   


