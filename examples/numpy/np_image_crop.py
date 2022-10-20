#filename: np_image_crop.py
#description: croping an image automatically with numpy

from PIL import Image
import numpy as np 
# from numpy import asarray

# load the image
image = Image.open('test.png')

#grayscale converter
image=image.convert('L')

# convert image to numpy array
imagedata = np.asarray(image)
print(type(imagedata))

# summarize shape
print(imagedata.shape)

# create Pillow image from the numpy array
image2 = Image.fromarray(imagedata)
print(type(image2))

# summarize image details
print(image2.mode)
print(image2.size)

#find location of the white pixels in the array
indices = np.where(imagedata >= [200])
print("coords of white pixels")
print(indices)
y1=int(np.amin(indices[0],axis=0))
x1=int(np.amin(indices[1],axis=0))
y2=int(np.amax(indices[0],axis=0))
x2=int(np.amax(indices[1],axis=0))
print (f"first pixel: {x1},{y1}")
print (f"last pixel: {x2+1},{y2+1}")
#output cropped image
new_image=image.crop((x1,y1,x2+1,y2+1))
new_image.save("test2.png")
