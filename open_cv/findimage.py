import pyautogui 
import os
import json

class FindImage:
  #class variables
   def __init__(self,json_file,message,top=None,bottom=None):
      self.path      = path=os.getcwd()
      self.json_file = json_file
      self.message   = message
      self.top       = top
      self.bottom    = bottom

   @staticmethod
   def  load_target_data_from_json(path,json_file,target_message):
     f=open(json_file)        #open file
     data = json.load(f)      #load json data into mem
     f.close                  #close file
     print(f"debug1: load_target_data_from_json -  source json file is #{json_file}")

     file_array=[]
     #loop through the json data
     for i in data:
      message=i['message']
      filename=i['filename']
      if i['message'] == target_message:
        print("debug2: load_target_data_from_json - appending " + path + filename )
        file_array.append(path + filename)
      return file_array

   @staticmethod
   def find_target_image_on_screen(image,top=None,bottom=None):
     if top==None or bottom==None:
       return pyautogui.locateOnScreen(image, confidence=0.81)
     else:
       return pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=0.81)

   @staticmethod
   def find_one_image_from_many_files(my_array,top=None,bottom=None):
    #print("find_one_image_from_many_files")
    for image in my_array:
      result=FindImage.find_target_image_on_screen(image,top,bottom)
      if result != None:
         return result,image #location result and imagefile
    return None,""

   @staticmethod
   def search_for_image_return_location(path,json_file,target,top=None,bottom=None):
     #nested function - not the best code
     result=None # default to none
     images=[]
     images=FindImage.load_target_data_from_json(path,json_file,target)
     result,imagefile=FindImage.find_one_image_from_many_files(images,top,bottom)
     return result,imagefile   


#messages_folder=(path + "/messages/") #message images
pwd=os.getcwd()
button_json=( pwd + "/buttons/" + "buttons.json")
result=FindImage.search_for_image_return_location(path=os.getcwd(),json_file=button_json,target="align",top=[0,0],bottom=[0,0])
