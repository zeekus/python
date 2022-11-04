class A(object):

    def foo(self,x):
        print(f"executing foo{self}, {x}")

    @classmethod
    def class_foo(cls,x):
        print(f"executing class_foo{cls}, {x}")

    @staticmethod
    def static_foo(x):
        print(f"executing static_foo({x})")


a=A() #initalize class
a.foo(1)
a.class_foo(2.5)
#class call
A.class_foo(3)
A.static_foo(4)

