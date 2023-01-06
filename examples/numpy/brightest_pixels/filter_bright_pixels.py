from PIL import Image
import numpy as np 

area = image[0:100, 0:100]
max_intensity = np.amax(area)
THRESHOLD = 200  # Adjust this value as needed
if max_intensity > THRESHOLD:
    print("There are pixels that are too bright to detect with OpenCV")

bright_indices = np.where(area > THRESHOLD) #indice of bright pixels
np.put(area, bright_indices, THRESHOLD) #indice of filtered pixes. 

# Convert the NumPy array to a PIL image
image = Image.fromarray(area)

# Save the image
image.save("filtered_image.png")
