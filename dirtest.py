class NN:
    def __init__(self):
        self.x = 10

    def foo(self, present=False):
        if present:
            print("fool")
        else:
            print("foo")
    def bar(self, present=False):
        print("bart")

a = NN()

object_methods = [method_name for method_name in dir(a)
                  if callable(getattr(a, method_name)) and method_name[0] != '_']

print(object_methods)
for m in object_methods:
    func = getattr(a, m)
    func(present=False)