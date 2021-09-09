"""
An example of creating a distance field using Manhattan distance
"""

GRID_HEIGHT = 6
GRID_WIDTH = 8


def manhattan_distance(row0, col0, row1, col1):
    """
    Compute the Manhattan distance between the cells
    (row0, col0) and (row1, col1)
    """
    return (abs(row0 - row1)) + (abs(col0 - col1))


def create_distance_field(entity_list):
    """
    Create a Manhattan distance field that contains the minimum distance to
    each entity (zombies or humans) in entity_list
    Each entity is represented as a grid position of the form (row, col)
    """
    # create grid using grid width and height
    grid = [[1000 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    # iterate through grid positions:
    for x in range(GRID_HEIGHT):
        print('x=', x)
        for y in range(GRID_WIDTH):
            print('y=', y)
            # compare distances to each entity
            for ent in entity_list:
                dist = manhattan_distance(x, y, ent[0], ent[1]) #abs(x - ent[0]) + abs(y - ent[1])
                print(dist)
                if dist < grid[x][y]:
                    grid[x][y] = dist
    # mark position as smallest number from entity
    return grid

def print_field(field):
    """
    Print a distance field in a human readable manner with
    one row per line
    """
    for x in field:
        print(x)


def run_example():
    """
    Create and print a small distance field
    """
    field = create_distance_field([[4, 0], [2, 5]])
    print_field(field)


run_example()

# Sample output for the default example
# [4, 5, 5, 4, 3, 2, 3, 4]
# [3, 4, 4, 3, 2, 1, 2, 3]
# [2, 3, 3, 2, 1, 0, 1, 2]
# [1, 2, 3, 3, 2, 1, 2, 3]
# [0, 1, 2, 3, 3, 2, 3, 4]
# [1, 2, 3, 4, 4, 3, 4, 5]