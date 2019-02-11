#!/usr/bin/env python
'''
Using a Class as a Decorator
'''

'''
def decorator(f):
    def helper():
        print("Decorating", f.__name__)
        f()
    return helper
'''

class decorator:
    def __init__(self, f):
        self.f = f
    def __call__(self):
        print("Decorating", self.f.__name__)
        self.f()

@decorator
def foo():
    print("inside foo()")

if __name__ == '__main__':
    foo()
