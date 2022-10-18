from PIL import Image

image = Image.open('image1.png')

#grayscale converter
grayscale=image.convert('L')

#Black and wite convert
BW=image.convert('1')

#save images
grayscale.save('grayscale_image.png')
BW.save('bw_image.png')
