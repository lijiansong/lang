#!/usr/bin/env python
'''
Classes instead of Functions:
the __call__ method
'''
class A:
    def __init__(self):
        print("An instance of A was initialized")

    def __call__(self, *args, **kwargs):
        print("Arguments are:", args, kwargs)

class Fibonacci:
    def __init__(self):
        self.cache = {}

    def __call__(self, n):
        if n not in self.cache:
            if n == 0:
                self.cache[0] = 0
            elif n == 1:
                self.cache[1] = 1
            else:
                self.cache[n] = self.__call__(n-1) + self.__call__(n-2)
        return self.cache[n]

if __name__ == '__main__':
    x = A()
    print("now calling the instance:")
    x(3, 4, x = 11, y = 10)
    print("Let's call it again:")
    x(3, 4, x = 11, y = 10)

    fib = Fibonacci()
    for i in range(40):
        print(fib(i), end=", ")
