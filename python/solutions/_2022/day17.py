import utils
from utils import SparseMatrix, Coord

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
SHAPES = [
    HLINE,
    PLUS,
    CORNER,
    VLINE,
    SQUARE,
]

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


def add_shape_to_tower(ii: int, jet_ii: int, grid: SparseMatrix, jets: str) -> (int, Shape):
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

    return jet_ii, shape


def build_tower(N_shapes: int, jets: str, grid: SparseMatrix):
    jet_ii = 0
    for ii in range(N_shapes):
        jet_ii, _ = add_shape_to_tower(ii, jet_ii, grid, jets)


def find_cycle(input: str) -> tuple[int, int, int, int]:
    jets = input
    grid = SparseMatrix()
    tower_height = 0
    history = dict()
    cycles = dict()
    jet_ii = 0
    for ii in range(9999999999999):
        shape_ii = ii % len(SHAPES)
        jet_ii, shape = add_shape_to_tower(ii, jet_ii, grid, jets)
        tower_height = max(y for x, y in grid)

        # make a unique id out of the shape id, x-position of the shape, and jet id
        hash = (shape_ii, min(x for x, y in shape), jet_ii)
        if hash in history:
            prev_height, prev_ii = history[hash]
            cycle_hash = (ii - prev_ii, tower_height - prev_height)
            if cycle_hash in cycles:
                return cycles[cycle_hash]

            cycles[cycle_hash] = (prev_ii, ii, prev_height, tower_height)
        history[hash] = (tower_height, ii)


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day17")
    grid1 = SparseMatrix()
    N = 2022
    build_tower(N, jets=input, grid=grid1)
    brute_height = max(y for x, y in grid1)
    return brute_height


@utils.profile
def part2():
    """Could probably improve this by detecting cycles on the fly instead of requiring a separate
    simulation for it. But that's a problem for Future Robin"""
    input = utils.load_puzzle_input("2022/day17")
    N = 1000000000000
    ii_from, ii_to, height_from, height_to = find_cycle(input)
    cycle_length = ii_to - ii_from
    cycle_height = height_to - height_from
    print(
        f"cycle detected from ii={ii_from}..{ii_to} (length {cycle_length}),"
        f"height={height_from=}..{height_to=} (length {cycle_height})"
    )
    startup = ii_from
    num_cycles, remainder = divmod((N - startup), cycle_length)
    shapes_to_simulate = startup + remainder
    print(f"After removing cycles, only need to simulate {shapes_to_simulate} shapes")
    grid2 = SparseMatrix()
    build_tower(shapes_to_simulate, jets=input, grid=grid2)
    simulated_height = max(y for x, y in grid2)
    height_from_cycles = cycle_height * num_cycles
    efficient_height = simulated_height + height_from_cycles
    return efficient_height


if __name__ == "__main__":
    assert part1() == 3109
    assert part2() == 1541449275365
