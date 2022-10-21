from PIL import Image, ImageDraw

def flood_fill(img):
  # Location of seed
  seed = (0, 0)
  
  # Pixel Value which would
  # be used for replacement
  rep_value = (0, 0, 0, 0)
  
  # Calling the floodfill() function and
  # passing it image, seed, value and
  # thresh as arguments
  ImageDraw.floodfill(img, seed, rep_value, thresh = 200)
  
  return img

# Opening the image and
# converting its type to RGBA
#img = Image.open(r"IMG_PATH").convert('RGBA')
img = Image.open("input.png").convert('RGBA')

img = flood_fill(img)  
  
#img.show()
img.save("result_img.png", "PNG")








