import pyautogui 
import os
import json
import re
import cv2

class FindImage:
   """ 
   A class for searching for images on the screen and returning their location.
    
    This class has three static methods: load_image_data_from_json, 
    search_for_image_and_return_location, and find_target_image_on_screen.
    
    Attributes:
        - json_file (str): The file path for a JSON file containing image data.
        - message (str): A message to use for searching for images.
        - top (tuple): The top coordinates for a region of the screen to search.
        - bottom (tuple): The bottom coordinates for a region of the screen to search.
        - c (float): The minimum confidence level required to consider an image a match.
   """

   @staticmethod
   def  load_image_data_from_json(json_file,message):
     """Load a list of file paths for images that match a message from a JSON file.
        
        Args:
            json_file (str): The file path for a JSON file containing image data.
            message (str): A message to use for searching for images.
        
        Returns:
            list: A list of file paths for images that match the message.
     """
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
     '''
     The method then iterates over the list of images and searches for each image on the screen using the
     locateOnScreen method from the pyautogui library. If the top and bottom arguments are provided, the
     method searches only in the specified region. Otherwise, it searches the entire screen. If the image
     is found with a confidence level at or above the specified threshold, the method returns the location        
     of the image as a tuple. If the image is not found or the confidence level is not high enough, the
     method continues iterating through the list of images until it either finds a match or exhausts the
     list. If no match is found, the method returns None.


     Args:
            json_file (str): The file path for a JSON file containing image data.
            message (str): A message to use for searching for images.
            top ( array ): optional - start x,y location for the image search
            bot (array ):  opional - end x,y for the image search
            c: ( float): optional - confidence level for the OpenCV image match

        Returns:
            Either
               - location_truple which holds the image left corner x,y  and w,h
            Or - None if no image is found
     '''
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