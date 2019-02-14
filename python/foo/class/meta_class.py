#!/usr/bin/env python3
import random

def print_module_attributes():
    # name of the class as a string
    cls = "random"
    all_attributes = [x for x in dir(eval(cls)) if not x.startswith("__") ]
    print("==> all attributes of random: {0:s}".format(str(all_attributes)))

    # filtering the callable attributes, i.e. the public methods of the class.
    methods = [x for x in dir(eval(cls)) if not x.startswith("__")
                              and callable(eval(cls + "." + x))]
    print('==> callable methods of random: {0:s}'.format(str(methods)))

    non_callable_attributes = [x for x in dir(eval(cls)) if not x.startswith("__")
                              and callable(eval(cls + "." + x))]
    print('==> non callable attributes of random: {0:s}'.format(str(non_callable_attributes)))

class FuncCallCounter(type):
    """ A Metaclass which decorates all the methods of the
        subclass using call_counter as the decorator
    """

    @staticmethod
    def call_counter(func):
        """ Decorator for counting the number of function
            or method calls to the function or method func
        """
        def helper(*args, **kwargs):
            helper.calls += 1
            return func(*args, **kwargs)
        helper.calls = 0
        helper.__name__= func.__name__

        return helper


    def __new__(cls, clsname, superclasses, attributedict):
        """ Every method gets decorated with the decorator call_counter,
            which will do the actual call counting
        """
        for attr in attributedict:
            if callable(attributedict[attr]) and not attr.startswith("__"):
                attributedict[attr] = cls.call_counter(attributedict[attr])

        return type.__new__(cls, clsname, superclasses, attributedict)

class A(metaclass=FuncCallCounter):

    def foo(self):
        pass

    def bar(self):
        pass

if __name__ == '__main__':
    print_module_attributes()

    x = A()
    print(x.foo.calls, x.bar.calls)
    x.foo()
    print(x.foo.calls, x.bar.calls)
    x.foo()
    x.bar()
    print(x.foo.calls, x.bar.calls)
