from PIL import Image, ImageDraw

  
# Opening the image and
# converting its type to RGBA
#img = Image.open(r"IMG_PATH").convert('RGBA')
img = Image.open("bg.png").convert('RGBA')
  
# Location of seed
seed = (0, 0)
  
# Pixel Value which would
# be used for replacement
rep_value = (0, 0, 0, 0)
  
# Calling the floodfill() function and
# passing it image, seed, value and
# thresh as arguments
ImageDraw.floodfill(img, seed, rep_value, thresh = 200)
  
#img.show()
img.save("result_img.png", "PNG")








