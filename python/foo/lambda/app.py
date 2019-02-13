#!/usr/bin/env python3


'''
Imagine an accounting routine used in a book shop. It works on a list with sublists, which look like this:

# Order Number	Book Title and Author	Quantity	Price per Item
# 34587	Learning Python, Mark Lutz	4	40.95
# 98762	Programming Python, Mark Lutz	5	56.80
# 77226	Head First Python, Paul Barry	3	32.95
# 88112	Einführung in Python3, Bernd Klein	3	24.99

1. Write a Python program, which returns a list with 2-tuples. Each tuple consists of a the order number and the product of the price per items and the quantity. The product should be increased by 10,- € if the value of the order is smaller than 100,00 €.
Write a Python program using lambda and map.

2. The same bookshop, but this time we work on a different list. The sublists of our lists look like this:
[ordernumber, (article number, quantity, price per unit), ... (article number, quantity, price per unit) ]
Write a program which returns a list of two tuples with (order number, total amount of order).
'''

if __name__ == '__main__':
    # problem 1 solution
    orders = [[34587, 'Learning Python, Mark Lutz', 4, 40.95],
            [98762, 'Programming Python, Mark Lutz', 5, 56.80],
            [77226, 'Head First Python, Paul Barry',3, 32.95],
            [88112, 'Einführung in Python3, Bernd Klein', 3, 24.99]]
    min_order = 100
    invoice_totals = list(map(lambda x: x if x[1] >= min_order else (x[0], x[1]+10),
            map(lambda x: (x[0], x[2]*x[3]), orders)))
    print(invoice_totals)

    # problem 2 solution
    from functools import reduce
    orders = [ [1, ("5464", 4, 9.99), ("8274",18,12.99), ("9744", 9, 44.95)],
	       [2, ("5464", 9, 9.99), ("9744", 9, 44.95)],
	       [3, ("5464", 9, 9.99), ("88112", 11, 24.99)],
               [4, ("8732", 7, 11.99), ("7733",11,18.99), ("88112", 5, 39.95)] ]
    min_order = 100
    invoice_totals = list(map(lambda x: [x[0]] + list(map(lambda y: y[1]*y[2], x[1:])), orders))
    print(invoice_totals)
    invoice_totals = list(map(lambda x: [x[0]] + [reduce(lambda a,b: a + b, x[1:])], invoice_totals))
    print(invoice_totals)
    invoice_totals = list(map(lambda x: x if x[1] >= min_order else (x[0], x[1] + 10), invoice_totals))
    print(invoice_totals)

