#!/usr/bin/env python

if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
    # Be more pythonic
    b = [' ' * 2 * (7 - i) + 'very' * i for i in a]
    for line in b:
        print(line)
