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


def add_shape_to_tower(
    ii: int,
    jet_ii: int,
    grid: SparseMatrix,
    jets: str,
) -> int:
    # spawn rock at correct x/y
    shape_ii = ii % len(SHAPES)
    shape = SHAPES[shape_ii]
    tower_height = max(y for x, y in grid) if grid else 0
    x = 2  # units away from left wall
    y = 4 + tower_height
    shape = tuple((a + x, b + y) for a, b in shape)

    # move rock
    collision = False
    while not collision:
        # rock is moved by jets
        jet = jets[jet_ii]
        if jet == ">":
            shape = move_right(shape, grid)
        else:
            shape = move_left(shape, grid)
        # rock falls
        shape, collision = fall(shape, grid)
        jet_ii = (jet_ii + 1) % len(jets)
    # add rock to tower
    for point in shape:
        grid[point] = "#"

    return jet_ii


def build_tower(N_shapes: int, jets: str, grid: SparseMatrix):
    jet_ii = 0
    for ii in range(N_shapes):
        jet_ii = add_shape_to_tower(ii, jet_ii, grid, jets)


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day17")
    grid = SparseMatrix()
    build_tower(2022, jets=input, grid=grid)
    return max(y for x, y in grid)


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
