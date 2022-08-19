import numpy as np
from PIL import Image
import os


def get_image(row_id, root='test'):
    """
    Converts an image number into the file path where the image is located, 
    opens the image, and returns the image as a numpy array.
    """
    user_path=(os.path.expanduser('~'))
    os.chdir(user_path)
    os.chdir(root)
    print ("current path is " + os.getcwd())
    new_path=os.getcwd() 
    filename = "{}.png".format(row_id)
    file_path = os.path.join(new_path, filename)
    print(f"file_path is {file_path}")
    img = Image.open(file_path)
    return np.array(img)

#main
row_id="input_image"
np_image=get_image(row_id)

print(np_image)

