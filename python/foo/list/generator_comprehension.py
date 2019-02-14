#!/usr/bin/env python3

'''
Generator comprehensions were introduced with Python 2.6. They are simply like a list comprehension but with parentheses - round brackets - instead of (square) brackets around it. Otherwise, the syntax and the way of working is like list comprehension, but a generator comprehension returns a generator instead of a list.
'''

if __name__ == '__main__':
    x = (x **2 for x in range(20))
    print(x)
    print(list(x))

    # Calculation of the prime numbers between 1 and 100 using the sieve of Eratosthenes
    noprimes = [j for i in range(2, 8) for j in range(i*2, 100, i)]
    print(noprimes)
    primes = [x for x in range(2, 100) if x not in noprimes]
    print(primes)
    from math import sqrt
    n = 100
    sqrt_n = int(sqrt(n))
    no_primes = [j for i in range(2, sqrt_n+1) for j in range(i*2, n, i)]

