#!/usr/bin/env python
'''
Use cases of decorators
'''

# Case 1: Checking Arguments with a Decorator
def argument_test_natural_number(f):
    def helper(x):
        if type(x) == int and x > 0:
            return f(x)
        else:
            raise Exception("Argument is not an integer")
    return helper

@argument_test_natural_number
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

# Case 2: Counting Function Calls with Decorators
def call_counter(func):
    def helper(*args, **_args):
        helper.calls += 1
        return func(*args, **_args)
    helper.calls = 0

    return helper

@call_counter
def succ(x):
    return x + 1

@call_counter
def mul1(x, y=1):
    return x*y + 1

from greeting_decorator import greeting
# Using wraps from functools
@greeting
def f(x):
    """ just some silly function """
    return x + 4

if __name__ == '__main__':
    # Case 1: Checking Arguments with a Decorator
    for i in range(1,10):
	print(i, factorial(i))
    #print(factorial(-1))

    # Case 2: Counting Function Calls with Decorators
    print(succ.calls)
    for i in range(10):
        succ(i)
    print(succ.calls)
    mul1(3, 4)
    mul1(4)
    mul1(y=3, x=2)
    print(mul1.calls)

    # Using wraps from functools
    f(10)
    print("function name: " + f.__name__)
    print("docstring: " + f.__doc__)
    print("module name: " + f.__module__)


