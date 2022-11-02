class Methods:

    
    # static method decorator
    @staticmethod
    # python static method
    def static_method():
        print("This is static method")
    # python non static method
    def nonstatic_method(self):
        print(f"This is not a static method {str(self)}")
Methods.static_method()
Methods.nonstatic_method("'data'")
