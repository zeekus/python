import pyautogui
from PIL import Image,ImageDraw


def best_confidence_first(image,top=None,bottom=None):
 for count in range(99,80,-1):
   c=count*0.01# change int to float
   value=pyautogui.locateOnScreen(image, region=(top[0],top[1], bottom[0], bottom[1]),confidence=c) #defined areas should have higher confidence
   print(f"{count}: {c}")
   if value!=None:
    return value

  
w,h=pyautogui.size()

top=[0,0]
bottom=[w,h]

img_file = input("File name: ")
img = Image.open(img_file)
print("image orginal dimentions:" + str(img.getbbox()))
location=best_confidence_first(img,top,bottom)
print(f"location is {location}")