# Written by *** for COMP9021
#
# Two functions to implement.
#
#
# The function picture() takes two integers as arguments,
# that you can assume are both at least equal to 1;
# it prints out a "picture", that note has no trailing
# spaces on any line.
#
# You might find the rstrip() string method useful. 
#
#
# The function list_of_tuples() takes a string as argument,
# that you can assume is the name of a file that exists
# in the working directory.
#
# The file can contain anywhere any number of blank lines
# (that is, lines containing an arbitrary number of spaces
# and tabs--an empty line being the limiting case).
#
# Nonblank lines are always of the form:
#                a:b!c
# with any number of spaces at the beginning and at the end of the line
# (possibly none) and any number of spaces around : and around !
# (possibly none).
# When a < b < c, a tuple is added to the list that is eventually
# returned.


def picture(m, n):
    print(((' ' + '/\\' * n + ' ') * m).rstrip())
    print(('/ ' + '_' * 2 * (n - 1) + ' \\') * m)
    print(('\\ ' + ' ' * 2 * (n - 1) + ' /') * m)
    print(((' ' + '\\/' * n + ' ') * m).rstrip())


def list_of_tuples(filename):
    with open(filename) as file:
        L = []
        for line in file:
            if line.isspace():
                continue
            first, rest = line.split(':')
            second, third = rest.split('!')
            first, second, third = int(first), int(second), int(third)
            if first < second < third:
                L.append((first, second, third))
        return L