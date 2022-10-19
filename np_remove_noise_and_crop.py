# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np 

#description: clean up image remove none white characters from a black a grayscale image. 
#source https://clay-atlas.com/us/blog/2020/11/28/python-en-package-pillow-convert-background-transparent/
#source https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil

def crop_image_with_np(image):
    imagedata=np.asarray(image)       #convert image to np array
    indices = np.where(imagedata>200) #bright colors
    xmin=int(np.amin(indices[1],axis=0))
    ymin=int(np.amin(indices[0],axis=0))
    xmax=int(np.amax(indices[1],axis=0))
    ymax=int(np.amax(indices[0],axis=0))
    return image.crop((xmin,ymin,xmax,ymax))

def cleanup_noise(image):
    # Transparency
    newImage = []
    for item in image.getdata():
     if item[:3] <= (235, 235, 235): # first three prixes less than this off white 
        newImage.append((0, 0, 0, 255)) #black
     else:
        #print(str(item))
        newImage.append(item)
    # pic=image.putdata(newImage) #put nparray back into image
    return newImage

image = Image.open('test.png')
image = image.convert('RGB')
print(image.mode)
image = cleanup_noise(image)
image = crop_image_with_np(image)

print(image.mode, image.size)
image.save('output1.png') #image
# cropped.save('output2.png') #image





