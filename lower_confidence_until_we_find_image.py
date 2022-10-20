#filename: lower_confidence_until_we_find_image.py
#descrption: uses pyautogui to find an image match we give it a image file and compare with another

import pyautogui
from PIL import Image

def get_center_x_y(x,y,w,h):
    x=x+int(w/2)
    y=y+int(y/2)
    return x,y

def lower_confidence_until_we_find(needle,haystack):
  v=.99 #99%
  loc = None
  while loc == None:
    print( f"confidence is {v}")
    loc=pyautogui.locate(needle, haystack, confidence=v, grayscale=True )
    v = round (v - .01,2)

  x,y,w,h=loc #convert box values
  return x,y,w,h,v

#put image in memory with PIL
haystack=Image.open("output1.png")
needle=Image.open("test.png")


#load image into memory
#loc,v=lower_confidence_until_we_find('output1.png','test.png')
x,y,w,h,v=lower_confidence_until_we_find(haystack,needle)
#print(f"location of image is {loc} with confidence of {v}")
#print(f"box is {type(loc)}")
print(f"x:{x},y:{y},width:{w},height:{h}")
x,y=get_center_x_y(x,y,w,h)
print(f"image center is at x:{x},y:{y}")


  
