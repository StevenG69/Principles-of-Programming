# Written by Eric Martin for COMP9021
#
# Here are the stripes of width 1 of length 2 (minimal), 3 and 4:
#
# *
#   *
#
# *
#   *
#     *
#
# *
#   *
#     *
#       *
#
# Here are the stripes of width 2 of length 2 (minimal), 3 and 4:
#
#   *
# *   *
#   *
#
#   *
# *   *
#   *   *
#     *
#
#   *
# *   *
#   *   *
#     *   *
#       *
#
# Here are the stripes of width 3 of length 2 (minimal), 3 and 4:
#
#     *
#   *   *
# *   *
#   *
#
#     *
#   *   *
# *   *   *
#   *   *
#     *
#
#     *
#   *   *
# *   *   *
#   *   *   *
#     *   *
#       *
#
# For a given width, returns the maximal size (required to be
# at least equal to 2 * width) of stripes of that width,
# the number of such stripes, and a grid that captures them.
#
# Note that stripes can overlap.


from random import seed, random
import sys


dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def stripes(width):
    # Points on the right boundary of a previously discovered stripe 
    to_ignore = set()
    stars_to_output = set()
    stripes_count = 0
    max_length = 0
    for i in range(dim - width):
        for j in range(width - 1, dim - 1):
            if (i, j) in to_ignore\
               or not strike(i, j, width)\
               or not strike(i + 1, j + 1, width):
                continue
            to_ignore.add((i + 1, j + 1))
            stars = set()
            add_stars(stars, i, j, width)
            add_stars(stars, i + 1, j + 1, width)
            i1, j1 = i + 1, j + 1
            while (i1 := i1 + 1) <= dim - width\
                  and (j1 := j1 + 1) < dim\
                  and strike(i1, j1, width):
                add_stars(stars, i1, j1, width)
                to_ignore.add((i1, j1))
            if i1 - i > max_length:
                max_length = i1 - i
                stripes_count = 1
                stars_to_output = stars
            elif i1 - i == max_length:
                stripes_count += 1
                stars_to_output.update(stars)
    return stripes_count, width * max_length,\
           [['*' if (i, j) in stars_to_output else ' '
                 for j in range(dim)
            ] for i in range(dim)
           ]
    
def strike(i, j, width):
    return all(grid[i + k][j - k] == '*' for k in range(width))

def add_stars(stars, i, j, width):
    stars.update((i + k, j - k) for k in range(width))
    
try:
    for_seed, width, density = input('Input an integer, an integer '
                                     'greater than 0,\n      and '
                                     'a number between 0 and 1: '
                                    ).split()

    for_seed, width, density = int(for_seed), int(width), float(density)
    if width < 1 or density < 0 or density > 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [['*' if random() < density else ' ' for _ in range(dim)]
             for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display(grid)

count, size, new_grid = stripes(width)
if not count:
    print(f'There are no stripes of width {width} in the grid!')
else:
    print(f'The size of the largest stripes of width is {size}.')
    print('There', count == 1 and 'is' or 'are', count,
          count == 1 and 'stripe' or 'stripes',
          'of that size.'
         )
    print('Here', count == 1 and 'it is:\n' or 'they are:')
    display(new_grid)
