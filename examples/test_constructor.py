class Example1:
    def __init__(self,*args):
      self.search=args[0]
      print(self.search)
      self.imageloc=get_location(self)

    def get_location(search):
      print(f"value is #{self.search}")
      self.imageloc=([0,0])

e1 = Example1("align")
print("String :",e1)

