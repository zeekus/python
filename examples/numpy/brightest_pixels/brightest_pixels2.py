import numpy as np

def find_brightest_pixels(image):

    '''
    This function takes a NumPy array image and returns a list of indices bright_indices of the brightest pixels in the image. 
    The brightness of a pixel is determined by its intensity value, which is the value of the pixel in the array.
    You can call this function on an image like this:'''
    
    # Find the indices of the brightest pixels
    bright_indices = np.argwhere(image == np.amax(image))
    
    return bright_indices



#call with the following
image = np.array([[0, 0, 0],
                  [0, 100, 0],
                  [0, 0, 255]])
bright_indices = find_brightest_pixels(image)
print(bright_indices)  # prints "[[2 2]]"
