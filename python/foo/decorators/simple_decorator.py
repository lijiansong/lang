#!/usr/bin/env python

'''
def our_decorator(func):
    """
    simple decorator
    """
    def function_wrapper(x):
        print("Before calling " + func.__name__)
        func(x)
        print("After calling " + func.__name__)
    return function_wrapper

def foo(x):
    print("Hi, foo has been called with " + str(x))

if __name__ == '__main__':
    print("We call foo before decoration:")
    foo("Hi")

    print("We now decorate foo with f:")
    foo = our_decorator(foo)

    print("We call foo after decoration:")
    foo(42)
'''

def our_decorator(func):
    def function_wrapper(x):
        print("Before calling " + func.__name__)
        res = func(x)
        print(res)
        print("After calling " + func.__name__)
    return function_wrapper

@our_decorator
def succ(n):
    return n + 1

@our_decorator
def foo(x):
    print("Hi, foo has been called with " + str(x))

from math import sin, cos

if __name__ == '__main__':
    succ(10)
    foo("Hi")
    sin = our_decorator(sin)
    cos = our_decorator(cos)
    for f in [sin, cos]:
        f(3.1415)
