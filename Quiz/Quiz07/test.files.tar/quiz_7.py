# Written by Hongyin Zhou for COMP9021
#
# Working with a grid of size 10 x 10, with i and j
# interpreted as follows:
#
#              j
#     1 2 3 4 5 6 7 8 9 10
#   1
#   2
#   3
#   4
# i 5
#   6
#   7
#   8
#   9
#  10
#
# Finds the longest path in the grid starting from (i, j),
# moving up diagonally in the NE direction (↗)
# or moving down diagonally in the SW direction (↙),
# moving SE to change direction.
#
# Moving up to start with.
#
# To make the path unique, we prefer moving in a given direction
# (up or down) for as long as possible.


from random import seed, random
import sys

dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def valid_move(i, j):
    return 0 <= i < dim and 0 <= j < dim

def dfs(row, col, grid, ne, path, visited):
    directions = [(-1, 1)] if ne else [(1, -1)]  # NE direction (↗) or SW direction (↙)
    change_direction = (1, 1)  # SE move for changing direction

    if not valid_move(row, col) or (row, col) in visited or grid[row][col] != '*':
        return path
  
    visited.add((row, col))
    path.append((row, col))
    longest_path = path

    # Explore in the current direction as far as possible
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if valid_move(new_row, new_col) and grid[new_row][new_col] == '*':
            new_path = dfs(new_row, new_col, grid, ne, path[:], visited)
            if len(new_path) > len(longest_path):
                longest_path = new_path

    # If no valid move in the current direction, try changing direction
    new_row, new_col = row + change_direction[0], col + change_direction[1]
    if valid_move(new_row, new_col) and grid[new_row][new_col] == '*':
        new_path = dfs(new_row, new_col, grid, not ne, path[:], visited)
        if len(new_path) > len(longest_path):
            longest_path = new_path

    return longest_path
    
def longest_path(i, j, grid):
    path = []
    visited = set()
    path = dfs(i - 1, j - 1, grid, True, path, visited)
    path_length = len(path)

    # Create a display grid for the path
    path_in_grid = [[' ' for _ in range(dim)] for _ in range(dim)]
    count = 0 
    for i in range(path_length - 1):
        x, y = path[i]
        next_x, next_y = path[i+1]
        path_in_grid[x][y] = '↗' if count % 2 == 0 else '↙'
        if next_x - x == 1 and next_y - y == 1:
            count += 1
        last_x, last_y = path[-1]
        path_in_grid[last_x][last_y] = '↗' if count % 2 == 0 else '↙'

    return path_length, path_in_grid

try:
    for_seed, i, j, density = input('Input an integer, two integers between '
                                    f'1 and {dim},\n      '
                                    'and a number between 0 and 1: '
                                   ).split()

    for_seed, i, j, density = int(for_seed), int(i), int(j), float(density)
    if i < 1 or i > dim or j < 1 or j > dim or density < 0 or density > 1:
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

path_length, path_in_grid = longest_path(i, j, grid)
if not path_length:
    print(f'There is no special path starting from ({i}, {j}) in the grid!')
else:
    print(f'The longest special path starting from ({i}, {j}) '
          f'has a length of {path_length}.'
          )
    print('Here it is:')
    display(path_in_grid)
