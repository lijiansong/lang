# An example of a class
class Shape:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = "This shape has not been described yet"
        self.author = "Nobody has claimed to make this shape yet"

    def area(self):
        return self.x * self.y

    def perimeter(self):
        return 2 * self.x + 2 * self.y

    def describe(self, text):
        self.description = text

    def authorName(self, text):
        self.author = text

    def scaleSize(self, scale):
        self.x = self.x * scale
        self.y = self.y * scale

    def showInfo(self):
        print("Shape info: {0:f}, {1:f}, {2:s}".format(self.x, self.y, self.description))

if __name__ == '__main__':
    rectangle = Shape(100, 45)
    print(rectangle.area())
    print(rectangle.perimeter())
    rectangle.describe("A wide rectangle, more than twice\
 as wide as it is tall")
    rectangle.scaleSize(0.5)
    print(rectangle.area())
    rectangle.showInfo()

