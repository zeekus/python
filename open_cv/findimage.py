import pyautogui 

class FindImage:
  #class variable
  location=None

  @classmethod
  def find_image(cls,image_name,screen_start=None,screen_end=None):
    #finding image on screen
    if screen_start==None or screen_end==None:
       cls.location=pyautogui.locateOnScreen(image_name,confidence=0.81) 
    else:
       cls.location=pyautogui.locateOnScreen(image_name,screen_start,screen_end,confidence=0.81) 
    print(f"The screen location for {image_name} is {cls.location}")

FindImage("testimage.png")
