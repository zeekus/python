class Button:
    def __init__(self,name,image_file,location=[]): #class method take more variables.
      self.name = name
      self.location = location
      self.image_file = image_file

    @classmethod
    def find_button_location(cls, name, image_file, location):
      location=[100,1000]
      return cls(name,image_file,location) #class method return sends back an object. 

    def show(self):
      print(self.name + " location:" + str(self.location))


e1 = Button("align","example.png",[10,0])
e1.show()
print("String :",e1)
align_info = Button.find_button_location('align','image.png',[0,0])
print(str(align_info))
print(str(align_info.location))

