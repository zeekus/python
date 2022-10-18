from PIL import Image
img = input("File name: ")
img = Image.open(img);
count = 0
fbpixel=[]#first bright pixel
lbpixel=[]#last bright pixel
lx=0 #lowest y
hx=0 #highest x
hy=0 #highest y

for y in range(img.height):
  for x in range(img.width):
   pixel = img.getpixel((x, y))
   #print (str(pixel) + ":" + str(x) + "," + str(y))
   if pixel[0] >= 200 and pixel[1] >=200 and pixel[2] >=200:
    if count<1:
      lx=x
      fbpixel=[x,y]
      print("* first pixel found at " + str(fbpixel))

    else:
      lbpixel=[x,y]
      if lx>x:
        lx=x
      if hy<y:
        hy=y
      if hx<x:
        hx=x
    count += 1
    print (str(pixel) + ":" + str(x) + "," + str(y))

print(count,"pixels are bright.")
print("first:" + str(lx) + "," + str(fbpixel[1]))
print(" last:" + str(hx) + "," + str(hy))

print("cropping image.")
img1=img.crop((lx,fbpixel[1],hx,hy))
img1.save('output2.png')