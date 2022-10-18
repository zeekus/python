from PIL import Image
import numpy as np

img = Image.open('bg.png')
data = np.array(img)

converted=np.where(data>200,200,200)
img=Image.fromarray(converted.astype('uint8'))

img.save('new_bg.png')

