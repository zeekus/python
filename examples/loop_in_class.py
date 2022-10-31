class Testloop:
    def __init__(self, iterations=0):
        self.iterations=iterations

    def for_loop(self):
      print(f"for loop with {self.iterations}")
      for x in range(self.iterations):
        print(x+1)

    def while_loop(self):
      print(f"while loop with {self.iterations}")
      x=1
      while x < self.iterations+1:
        print(x)
        x+=1

myloop=Testloop(5)
myloop.for_loop()
myloop.while_loop()