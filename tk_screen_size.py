#!/usr/bin/python
#filename: tk_screen_size.py
#description: get screensize of tk

import tkinter
import pyscreenshot as ImageGrab 
import numpy as np

my_window=tkinter.Tk()
w=my_window.winfo_screenwidth()
h=my_window.winfo_screenheight()
print(f"our screen size is w: {w},h: {h}")

#full screen
print("getting full image")
full_image=ImageGrab.grab(bbox=(0,0,w,h)).convert("L")
#convert to numpy
img_np_full=np.array(full_image)
y,x=img_np_full.shape
print(f"full image has the numpy shape of {img_np_full.shape}")
print(f"full image has and x,y of {x},{y}")

#get part of the screen 
print(f"getting partial image from a start of 300,400 and {w},{h}")
my_image=ImageGrab.grab(bbox=(300,400,w,h)).convert("L")
img_np=np.array(my_image)
y,x=img_np.shape 
print(f"our partial image has the numpy shape of {img_np.shape}")
print(f"our partial image has and x,y of {x},{y}")

