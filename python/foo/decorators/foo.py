#!/usr/bin/env python

import math

def succ(x):
    return x + 1

# functions inside functions
def temperature(t):
    def celsius2fahrenheit(x):
        return 9 * x / 5 + 32

    result = "It's " + str(celsius2fahrenheit(t)) + " degrees!"
    return result

# functions as paramaters
def foo(func):
    print("The function " + func.__name__ + " was passed to foo")
    res = 0
    for x in [1, 2, 2.5]:
        res += func(x)
    return res

# functions returning functions
def polynomial_creator(*coefficients):
    """ coefficients are in the form a_0, a_1, ... a_n
    """
    def polynomial(x):
        res = 0
        for index, coeff in enumerate(coefficients):
            res += coeff * x** index
        return res
    return polynomial


if __name__ == '__main__':
    successor = succ
    print(successor(10))
    del succ
    print(successor(10))

    # functions inside functions
    print(temperature(20))

    # functions as paramaters
    print(dir(math))
    print(foo(math.sin))
    print(foo(math.cos))

    # functions returning functions
    p1 = polynomial_creator(4)
    p2 = polynomial_creator(2, 4)
    p3 = polynomial_creator(2, 3, -1, 8, 1)
    p4  = polynomial_creator(-1, 2, 1)
    for x in range(-2, 2, 1):
        print(x, p1(x), p2(x), p3(x), p4(x))
