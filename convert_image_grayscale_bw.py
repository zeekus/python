from PIL import Image

image = Image.open('__warpto0.png')

#grayscale converter
grayscale=image.convert('L')

#Black and wite convert
BW=image.convert('1')

#save images
grayscale.save('__warpto2.png')
#BW.save('__warpto2.png') #scatter type
