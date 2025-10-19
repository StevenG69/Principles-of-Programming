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
    #Top boundary
    print(((' ' + r"/\ ".rstrip() * n + ' ') * m).rstrip())
    #2nd boundary
    print((r"/ ".rstrip() + ' ' + '_' * 2 * (n - 1) + " " + r"\ ".rstrip()) * m)
    #3rd boundary
    print((r"\ ".rstrip() + ' ' * 2 * n + r"/ ".rstrip()) * m)
    #Bottom boundary
    print(((' ' + r"\/ ".rstrip() * n + ' ') * m).rstrip())

    # REPLACE PASS ABOVE WITH YOUR CODE


def list_of_tuples(filename):
    L = []

    with open(filename) as file:
        for line in file:
            # Skip blank lines
            if not line.isspace():
                # Remove leading and trailing whitespace
                line = line.strip()

                # Split the line using ':' and '!' and remove extra spaces
                a, b_c = line.split(':')
                b, c = b_c.split('!')

                # Strip spaces around the values and convert to integers
                a = int(a.strip())
                b = int(b.strip())
                c = int(c.strip())

                # Add to list if a < b < c
                if a < b < c:
                    L.append((a, b, c))

    # print(L)  # Print the final list after processing
    return L

    # REPLACE THE RETURN ABOVE WITH YOUR CODE
