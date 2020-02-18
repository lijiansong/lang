#!/usr/bin/env python

if __name__ == '__main__' :
    ages = {}

    ages['Sue'] = 23
    ages['Peter'] = 19
    ages['Andrew'] = 78
    ages['Karren'] = 45

    if 'Sue' in ages:
        print ("Sue is in the dictionary. She is", \
    ages['Sue'], "years old")

    else:
        print ("Sue is not in the dictionary")

    print ("The following people are in the dictionary:")
    print (ages.keys())

    keys = ages.keys()

    print ("People are aged the following:", \
    ages.values())

    values = ages.values()

    print keys
    print(sorted(keys))

    print values
    print(sorted(values))

    print ("The dictionary has", \
    len(ages), "entries in it")
