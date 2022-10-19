# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np 

#description: clean up image remove none white characters from a black a grayscale image. 
#source https://clay-atlas.com/us/blog/2020/11/28/python-en-package-pillow-convert-background-transparent/
#source https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil

#def crop_image_only_outside(img,tol=0):
#    # img is 2D image data
#    # tol  is tolerance
#    mask = img>tol
#    m,n = img.shape
#    mask0,mask1 = mask.any(0),mask.any(1)
#    col_start,col_end = mask0.argmax(),n-mask0[::-1].argmax()
#    row_start,row_end = mask1.argmax(),m-mask1[::-1].argmax()
#    return img[row_start:row_end,col_start:col_end]

image = Image.open('test.png')
image = image.convert('RGB')
print(image.mode)

# Transparency
newImage = []
for item in image.getdata():
    if item[:3] <= (235, 235, 235): # first three prixes less than this off white 
        newImage.append((0, 0, 0, 255)) #black
    else:
        print(str(item))
        newImage.append(item)
image.putdata(newImage)

print(image.mode, image.size)
image.save('output1.png') #image
# cropped.save('output2.png') #image





