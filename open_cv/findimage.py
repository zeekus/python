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
   def find_target_image_on_screen(image,top=None,bottom=None):
     if top==None or bottom==None:
       return pyautogui.locateOnScreen(image, confidence=0.75)
     else:
       pyautogui.moveTo(top[0],top[1])
       return pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=0.85) #static is good enough

   @staticmethod
   def return_image_location_from_array(my_array,top=None,bottom=None):
    fail_count=0
    result=None
    for image in my_array:
      result=FindImage.find_target_image_on_screen(image,top,bottom)
      if result != None:
        #print(f"return_image_location_from_array: result is {result}")
        return result,image #location result and imagefile
      else:
        fail_count=fail_count+1
        #print(f"Debug: return_image_location_from_array: {image} - {fail_count}")
    return None,""

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
   def search_for_image_and_return_location(json_file,message,top=None,bottom=None):
     result=None # default to none
     images=[]
     #print(f"debug: search_for_image_and_return_locatin - searching for a {message}")
     images=FindImage.load_image_data_from_json(json_file,message)
     result,imagefile=FindImage.return_image_location_from_array(images,top,bottom)
     return result,imagefile   


