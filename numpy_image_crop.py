#filename: numpy_image_cropping.py
#description: generates and crops an image with numpy and PIL

import numpy as np
from PIL import Image  

#generate a 100/100 pixel array of zeros
#a 10/10 black square
zeros = np.zeros((100, 100), dtype=np.uint8)

#draw a line in the first row of the image 2 pixels wide
#zeros[:-1,:2] = 255 #horizonal line 2 pixels deep
#zeros[:2,:-1] = 255 #vertical line 2 pixels deep from top
zeros[-5,:-1] = 255  #vertical line 5 pixels from the bottom row

#create PIL image from the np array and save it
image = Image.fromarray(zeros)
image.save("test1.png")

#find location of the white pixels in the array
indices = np.where(zeros >= [200])
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

