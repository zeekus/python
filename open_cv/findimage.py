import pyautogui 
import os
import json
import re

class FindImage:

  # too slow
  #  @staticmethod
  #  def find_target_image_on_screen(image,top=None,bottom=None):
  #    if top==None or bottom==None:
  #      return pyautogui.locateOnScreen(image, confidence=0.81)
  #    else:
  #      image_found=None
  #      for countdown in range(99,80,-3):
  #        c=round(countdown*0.01,2) # change int to float with 2 places
  #        image_found=pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=c) #defined areas should have higher confidence
  #        #print(f"{count}: {c}")
  #        if image_found!=None:
  #          print(f"Debug: find_target_image_on_screen - Image name is {image}")
  #          print(f"Debug: find_target_image_on_screen - confidence {c}: top: {top}, bottom {bottom} - image box is {image_found}")
  #          return image_found


   @staticmethod
   def  load_image_data_from_json(json_file,message):
    #  print(f"debug1: load_image_data_from_json -  source json file is '{json_file}'")
    #  print(f"debug2: load_image_debug_from_json {message}")
     count=0
     f=open(json_file)        #open file
     data = json.load(f)      #load json data into mem
     f.close                  #close file
     file_array=[]

     #if re.search('button',json_file) or re.search('yellow',message):
     if re.search('/buttons/',json_file):                                                                            
       filetype="buttons"
     elif re.search('/session/',json_file):                                                                            
       filetype="session"
     else:
       filetype="messages"
                                                                                     
     for i in data:
      if re.search( message, i['message']):
        fullpath=(f"{os.getcwd()}/{filetype}/{i['filename']}")
        count=count+1
        file_array.append(fullpath)

     #print(f"Debug: load_image_data_from_json: {message} image count was {count}")
     return file_array

   @staticmethod
   def search_for_image_and_return_location(json_file,message,top=None,bottom=None,c=0.79):
     location_tuple=None # default to none
     images=[]
     #print(f"debug: search_for_image_and_return_locatin - searching for a {message}")
     images=FindImage.load_image_data_from_json(json_file,message) #get list of images to search 
     for image in images:
          if top==None or bottom==None:
            location_tuple=pyautogui.locateOnScreen(image,confidence=c)
            #print(f"search_for_image_and_return_location debug-1: {image}: {message}: {location_tuple}")
          else:
            location_tuple=pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=c) #static is good enough
            #print(f"search_for_image_return_location debug-2: {image} : {message} : {location_tuple}")
          if location_tuple is not None: 
            return location_tuple
     return location_tuple 


