#!/usr/bin/env python

from moduletest import ageofqueen
from moduletest import printhello

from mod import shape as s

import math

if __name__ == '__main__':
    print(ageofqueen)
    printhello()

    rectangle = s.Shape(100, 45)
    print(rectangle.area())
    print(rectangle.perimeter())
    rectangle.describe("A wide rectangle, more than twice\
 as wide as it is tall")
    rectangle.scaleSize(0.5)
    print(rectangle.area())
    rectangle.showInfo()

    print(dir(math))


