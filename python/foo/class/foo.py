#!/usr/bin/env python

class A:
    def __str__(self):
        return 'A'

if __name__ == '__main__':
    print(A.__dict__)
    a = A()
    print(str(a))
