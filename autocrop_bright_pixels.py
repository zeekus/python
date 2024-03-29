from PIL import Image,ImageOps



def crop_on_bright_pixel_edges(img):
  count = 0
  fbpixel=[]#first bright pixel
  lbpixel=[]#last bright pixel
  lx=0 #lowest y
  hx=0 #highest x
  hy=0 #highest y
  for y in range(img.height):
    for x in range(img.width):
     pixel = img.getpixel((x, y))
     if pixel[0] >= 200 and pixel[1] >=200 and pixel[2] >=200: #bright pixel
       if count<1:
         lx=x
         fbpixel=[x,y]
         #print("* first pixel found at " + str(fbpixel))
       else:
         lbpixel=[x,y]
         if lx>x:
          lx=x
         if hy<y:
          hy=y
         if hx<x:
          hx=x
       count += 1
       #print (str(pixel) + ":" + str(x) + "," + str(y))

  print(count,"pixels are bright.")
  print("first bright pixel:" + str(lx) + "," + str(fbpixel[1]))
  print(" last bright pixel:" + str(hx) + "," + str(hy))

  print("cropping image.")
  return img.crop((lx,fbpixel[1],hx+1,hy+1))
  
img_file = input("File name: ")
img = Image.open(img_file);
print("image orginal dimentions:" + str(img.getbbox()))
img_cropped=crop_on_bright_pixel_edges(img)
print("image cropped dimentions:" + str(img_cropped.getbbox()))
img_cropped.save('cropped_' + img_file)

# test=ImageOps(img_file,border=0)
# test.save('cropped_' + img_file)