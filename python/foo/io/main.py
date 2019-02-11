#!/usr/bin/env python


if __name__ == '__main__':

    '''
    fh = open("example.txt", "w")
    fh.write("To write or not to write\nthat is the question!\n")
    fh.close()
    '''
    with open("example.txt", "w") as fh:
        fh.write("To write or not to write\nthat is the question!\n")

    with open("ad_lesbiam.txt") as fobj:
        for line in fobj:
            print(line.rstrip())

    poem = open("ad_lesbiam.txt").readlines()
    print(poem)
    print(type(poem))

    poem = open("ad_lesbiam.txt").read()
    print(poem)
    print(type(poem))
