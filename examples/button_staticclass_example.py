class Find_Button:
    def __init__(self,name):
      self.name = name

    @staticmethod
    def find_button_location2(name):
      location=[1000,1000]
      print(f"button name is {name} location is {location}")
      return location
    
    def show(self):
      print(self.name + " location:" + str(self.location))


align_location=Find_Button.find_button_location2('align')
