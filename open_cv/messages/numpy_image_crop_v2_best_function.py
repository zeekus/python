#filename: numpy_image_cropping.py
#description: generates and crops an image with numpy and PIL

import numpy as np
from PIL import Image  

def crop_image(image):
  image=img.convert('L') #grayscale convert
  imagedata = np.asarray(image) #convert PIL image to numpy array
  indices = np.where(imagedata>= [200])
  #print("coords of white pixels")
  #print(indices)
  #find location of the white pixels in the array
  y1=int(np.amin(indices[0],axis=0))
  x1=int(np.amin(indices[1],axis=0))

  y2=int(np.amax(indices[0],axis=0))
  x2=int(np.amax(indices[1],axis=0))
  print (f"first pixel: {x1},{y1}")
  print (f"last pixel: {x2+1},{y2+1}")
  #output cropped image
  new_image=image.crop((x1,y1,x2+1,y2+1))
  return new_image #return cropped image

#main
img_file = input("File name: ")
img = Image.open(img_file);
print("image orginal dimentions:" + str(img.getbbox()))
new_image=crop_image(img)
print("image croped dimentions:" + str(new_image.getbbox()))
new_image.save("cropped__" + img_file)

