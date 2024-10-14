class triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return (self.base*self.height)/2
    

triangle1 = triangle(5, 30)
area = triangle1.area()
print(area)