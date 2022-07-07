import pyautogui
import inspect #look at objects
import time
import numpy as np
import json
import yaml

def pointer_location():
    x,y=pyautogui.position()
    return x,y

def pixel_color(x,y):
    color = pyautogui.pixel(x,y)
    return (color) #RGB int

def rgb_to_hex(r, g, b):
  return ('{:X}{:X}{:X}').format(r, g, b)

#dataset=

secs=10
later=time.time()+secs
count=0
print("map the colors of the blue bar.")
while  later > time.time():
    count=count+1
    x,y=pointer_location()
    rgb=pixel_color(x,y)
    r=rgb.red
    g=rgb.green
    b=rgb.blue
    hex_color=rgb_to_hex(r,g,b)
    print(str(count) + ":" + str(r),str(g),str(b) + ":" + hex_color )
    
    time.sleep(1)
