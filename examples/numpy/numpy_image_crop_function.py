#!/usr/bin/python
#filename: np_image_flatten.py
#description: convert image of text in cropped and black white. Source can be any color as long as Text is white.

# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np 

#description: clean up image remove none white characters from a black a grayscale image. 
#source https://clay-atlas.com/us/blog/2020/11/28/python-en-package-pillow-convert-background-transparent/
#source https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil


def crop_image_with_np(image):
    print("crop_image_with_np")
    imagedata=np.asarray(image)       #convert image to np array
    indices = np.where(imagedata>200) #bright colors
    xmin=int(np.amin(indices[1],axis=0))
    ymin=int(np.amin(indices[0],axis=0))
    xmax=int(np.amax(indices[1],axis=0))
    ymax=int(np.amax(indices[0],axis=0))
    return image.crop((xmin,ymin,xmax+1,ymax+1))

my_file=('/home/ted/Documents/git/python/open_cv/buttons/_bu_docking_system.png')
image = Image.open(my_file)
#image = flatten_image(image)
image = crop_image_with_np(image)
image.save('output1.png') #save newly processed image
