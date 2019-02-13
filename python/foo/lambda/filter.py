#!/usr/bin/env python


if __name__ == '__main__':
    fibonacci = [0,1,1,2,3,5,8,13,21,34,55]
    odd_numbers = list(filter(lambda x: x % 2, fibonacci))
    print(odd_numbers)
    even_numbers = list(filter(lambda x: x % 2 == 0, fibonacci))
    print(even_numbers)
    even_numbers = list(filter(lambda x: x % 2 -1, fibonacci))
    print(even_numbers)
