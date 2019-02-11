#!/usr/bin/env python

'''
Summarizing we can say that a decorator in Python is a callable Python object
that is used to modify a function, method or class definition. The original
object, the one which is going to be modified, is passed to a decorator
as an argument. The decorator returns a modified object, e.g. a modified
function, which is bound to the name used in the definition.
'''
from random import random, randint, choice

def our_decorator(func):
    def function_wrapper(*args, **kwargs):
        print("Before calling " + func.__name__)
        res = func(*args, **kwargs)
        print(res)
        print("After calling " + func.__name__)
    return function_wrapper

if __name__ == '__main__':
    random = our_decorator(random)
    randint = our_decorator(randint)
    choice = our_decorator(choice)

    random()
    randint(3, 8)
    choice([4, 5, 6])

