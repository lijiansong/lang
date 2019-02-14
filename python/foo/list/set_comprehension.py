#!/usr/bin/env python3

'''
A set comprehension is similar to a list comprehension, but returns a set and not a list. Syntactically, we use curly brackets instead of square brackets to create a set. Set comprehension is the right functionality to solve our problem from the previous subsection. We are able to create the set of non primes without doublets.
'''

def primes(n):
    if n == 0:
        return []
    elif n == 1:
        return []
    else:
        p = primes(int(sqrt(n)))
        no_p = {j for i in p for j in range(i*2, n+1, i)}
        p = {x for x in range(2, n + 1) if x not in no_p}
    return p

if __name__ == '__main__':
    from math import sqrt
    n = 100
    sqrt_n = int(sqrt(n))
    no_primes = {j for i in range(2, sqrt_n+1) for j in range(i*2, n, i)}
    print(no_primes)

    for i in range(1,50):
        print(i, primes(i))
