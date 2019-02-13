#!/usr/bin/env python

from functools import reduce

if __name__ == '__main__':
    # Determining the maximum of a list of numerical values by using reduce
    f = lambda a, b: a if (a > b) else b
    print(reduce(f, [47,11,42,102,13]))
    # Calculating the sum of the numbers from 1 to 100
    print(reduce(lambda x, y: x+y, range(1,101)))
    # calculate the product (the factorial) from 1 to a number
    print(reduce(lambda x, y: x*y, range(1,101)))
    print(type(reduce(lambda x, y: x*y, range(1,101))))

    print(reduce(lambda x, y: x*y, range(44,50))/reduce(lambda x, y: x*y, range(1,7)))
