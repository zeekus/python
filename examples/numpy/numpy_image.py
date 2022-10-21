

import cv2
import numpy as np

#image = Image.open('output1.png')
#image = image.convert('RGBA')

image= cv2.imread("output1.png")
image_arr = np.array(image) #convert image to array

temp=(image_arr==255).all(axis=-1)
white_pixels=np.asarray(np.where(temp)).T
first_white_pixel=white_pixels[:1]
last_white_pixel=white_pixels[:,-1]

# counting the number of pixels
number_of_white_pix = np.sum(image_arr == 255)
number_of_black_pix = np.sum(image_arr == 0)
  
print('Number of white pixels:', number_of_white_pix)
print('Number of black pixels:', number_of_black_pix)

print("first:" + str(first_white_pixel[0,1]))
print("last:" + str(last_white_pixel[0,1]))

