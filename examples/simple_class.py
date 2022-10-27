#!/usr/bin/python3

class SimpleExample():
  
    def __init__(self,name="no name"):
        self.name = name 

    def say_hi(self):
        print(f"Hi my name is '{self.name}'") #python3
    
p=SimpleExample('Bob')
p.say_hi()
p1=SimpleExample()
p1.say_hi()