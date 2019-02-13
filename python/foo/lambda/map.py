#!/usr/bin/env python

from math import sin, cos, tan, pi

'''
def map_functions(x, functions):
    """ map an iterable of functions on the the object x """
    res = []
    for func in functions:
        res.append(func(x))
    return res
'''

# be more pythonic
def map_functions(x, functions):
    """Mapping a List of Functions"""
    return [func(x) for func in functions]

if __name__ == '__main__':
    family_of_functions = [sin, cos, tan]
    print(map_functions(pi, family_of_functions))

    C = [39.2, 36.5, 37.3, 38, 37.8]
    F = list(map(lambda x: float(9)/5*x + 32, C))
    print(F)
    C = list(map(lambda x: float(5)/9*(x-32), F))
    print(C)

    # python3: multiple lists with different length
    a = [1, 2, 3, 4]
    b = [17, 12, 11, 10]
    c = [-1, -4, 5, 9, -1, -4, 5, 9]
    print(list(map(lambda x, y: x + y, a, b)))
    print(list(map(lambda x, y, z: x + y + z, a, b, c)))
    print(list(map(lambda x, y, z : 2.5*x + 2*y - z, a, b, c)))
