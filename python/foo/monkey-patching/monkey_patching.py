#!/usr/bin/env python

'''
monkey patch only refers to dynamic modifications of a class or module at run-time.
'''

import m

def monkey_f(self):
    print("monkey_f")

if __name__ == '__main__':
    m.A.f = monkey_f
    obj = m.A()
    obj.f()
