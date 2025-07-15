class Parent:
    def __init__(self, number):
        self.number = number
    
class Child(Parent):
    def __init__(self, number):
        super().__init__(number)

    def a(self):
        return self.number

def main():
    a = Child(4)
    print(a.a())
main()