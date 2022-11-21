class FindButton:
    def __init__(self,name):
      self.name = name

    @staticmethod
    def find_location(name):
      
      location=[1000,1000]
      print(f"button name is '{name}' coords are at '{location}'")
      return location
 



align_button=FindButton.find_location('align')
print(align_button)

