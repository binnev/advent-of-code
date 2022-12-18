import itertools

from python import utils
from python._2022.day14 import print_sparse_matrix, SparseMatrix, Coord

Shape = tuple[Coord, ...]
HLINE: Shape = (
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
)
PLUS: Shape = (
    (1, 0),
    (0, 1),
    (1, 1),
    (1, 1),
    (1, 2),
    (2, 1),
)
CORNER: Shape = (
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
)
VLINE: Shape = (
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
)
SQUARE: Shape = (
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
)
SHAPES = [HLINE, PLUS, CORNER, VLINE, SQUARE]

example = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


def move_left(shape: Shape, grid: SparseMatrix) -> Shape:
    new_shape = tuple((x - 1, y) for x, y in shape)
    for x, y in new_shape:
        if grid.get((x, y)) or x < 0:
            return shape  # don't move
    return new_shape


def move_right(shape: Shape, grid: SparseMatrix) -> Shape:
    new_shape = tuple((x + 1, y) for x, y in shape)
    for x, y in new_shape:
        if grid.get((x, y)) or x > 6:
            return shape
    return new_shape


def fall(shape: Shape, grid: SparseMatrix) -> (Shape, bool):
    collision = False
    new_shape = tuple((x, y - 1) for (x, y) in shape)
    for (x, y) in new_shape:
        if grid.get((x, y)) or y == 0:
            collision = True
            return shape, collision
    return new_shape, collision


def draw_moving_shape(shape: Shape, grid: SparseMatrix):
    for pt in shape:
        grid[pt] = "@"
    print_sparse_matrix(grid, flip_y=True, pad=2)
    for pt in shape:

        grid.pop(pt, None)


def add_column(grid: SparseMatrix):
    for x in range(7):
        grid[(x, 0)] = str(x + 1)
    # for x in [-1, 7]:
    #     grid[(x, 0)] = "+"
    # for y in range(1, 10):
    #     grid[(-1, y)] = grid[(7, y)] = "|"


@utils.profile
def part1():
    """
    3068 too low
    """
    # input = example
    input = utils.load_puzzle_input("2022/day17")
    jets = itertools.cycle(input)
    grid = SparseMatrix()
    add_column(grid)

    tower_height = 0
    for ii in range(2022):
        # spawn rock at correct x/y
        shape = SHAPES[ii % len(SHAPES)]
        x = 2  # units away from left wall
        y = 4 + tower_height
        shape = tuple((a + x, b + y) for a, b in shape)
        # draw_moving_shape(shape, grid)

        # move rock
        collision = False
        while not collision:
            # rock is moved by jets
            jet = next(jets)
            if jet == ">":
                # print("rock moves right")
                shape = move_right(shape, grid)
            else:
                # print("rock moves left")
                shape = move_left(shape, grid)
            # draw_moving_shape(shape, grid)
            # rock falls
            shape, collision = fall(shape, grid)
            # print("rock falls")
            # draw_moving_shape(shape, grid)

        # add rock to tower
        for point in shape:
            grid[point] = "#"
        tower_height = max(y for (x, y), value in grid.items() if value == "#")

    # print_sparse_matrix(grid, flip_y=True)
    return max(y for x, y in grid)


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
