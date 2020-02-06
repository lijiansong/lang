#!/usr/bin/env python3

'''

List comprehension is an elegant way to define and create list in Python. These lists have often the qualities of sets, but are not in all cases sets.
List comprehension is a complete substitute for the lambda function as well as the functions map(), filter() and reduce(). For most people the syntax of list comprehension is easier to be grasped.
'''

if __name__ == '__main__':
    # Filtered list comprehensions
    print([(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2])
    colours = [ "red", "green", "yellow", "blue" ]
    things = [ "house", "car", "tree" ]
    coloured_things = [ (x,y) for x in colours for y in things ]
    print(coloured_things)

