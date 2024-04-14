import math

class Figure:
    
    def __init__(self, type):
        self.type = type

    def get_type_figure(self):
        return self.type

class Circle(Figure):

    def __init__(self, type, radius = 0):
        super().__init__(type)
        
        self.radius = radius

    def area_circle(self):
        res = math.pi * math.pow(self.radius, 2)
        return res
    
class Triangle(Figure):

    def __init__(self, type, a = 0, b = 0, c = 0):
        super().__init__(type)

        self.a = a
        self.b = b
        self.c = c

    def area_triangle(self):
        p = (self.a + self.b + self.c)/2
        s = math.sqrt(p  * (p - self.a) * (p - self.b) * (p - self.c))
        return s
    
    def isRectangle(self):
        sum_kat = math.pow(self.a, 2) + math.pow(self.b, 2)
        gip = math.pow(self.c, 2)

        if sum_kat == gip:
            return True
        else:
            return False
        
def area_circle(radius):
    circle = Circle('circle', radius)

    return circle.area_circle()

def area_triangle(a, b, c):
    triangle = Triangle('triangle', a, b, c)

    return triangle.area_triangle()
