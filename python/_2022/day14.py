from functools import reduce
import numpy
from python import utils

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


Coord = tuple[int, int]
SparseMatrix = dict[Coord, str]


def draw_line(start: Coord, end: Coord, grid: SparseMatrix):
    start_x, start_y = start
    end_x, end_y = end
    dy = end_y - start_y
    start_x, end_x = min(start_x, end_x), max(start_x, end_x)
    start_y, end_y = min(start_y, end_y), max(start_y, end_y)

    if dy == 0:
        for x in range(start_x, end_x + 1):
            grid[(x, start_y)] = "#"
    else:
        for y in range(start_y, end_y + 1):
            grid[(start_x, y)] = "#"


def parse_input(input: str) -> SparseMatrix:
    instructions = input.splitlines()
    grid = SparseMatrix()
    for ins in instructions:
        points = [tuple(map(int, pair.split(","))) for pair in ins.split(" -> ")]
        for ii in range(len(points) - 1):
            start = points[ii]
            end = points[ii + 1]
            draw_line(start, end, grid)
    return grid


def print_sparse_matrix(grid: SparseMatrix, flip_y=False, pad=0):
    if grid:
        xs = [x for x, y in grid]
        ys = [(-y if flip_y else y) for x, y in grid]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
    else:
        min_x = max_x = min_y = max_y = 0
    for y in range(min_y - pad, max_y + 1 + pad):
        for x in range(min_x - pad, max_x + 1 + pad):
            print(grid.get((x, (-y if flip_y else y)), "."), end="")
        print("")
    print("")


def sand_step(pos: Coord, grid: SparseMatrix, floor: int = None) -> Coord | None:
    """Return new Coord if still falling; return None if came to rest."""
    x, y = pos
    options = [
        (x, y + 1),  # down
        (x - 1, y + 1),  # down_left
        (x + 1, y + 1),  # down_right
    ]
    # try to move in order of preference
    for (x, y) in options:
        if grid.get((x, y)) is None and y != floor:
            return (x, y)
    return None  # if all are blocked, come to rest


def sand_trace(origin: Coord, grid: SparseMatrix, abyss: int = None, floor: int = None) -> bool:
    """
    Return True if sand came to rest OK, False if it fell off the map
    """
    pos = origin

    while True:
        new_pos = sand_step(pos, grid, floor=floor)

        # came to rest
        if new_pos is None:
            grid[pos] = "o"
            return True

        # fall into abyss
        x, y = new_pos
        if abyss is not None and y > abyss:
            return False

        pos = new_pos


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day14")
    grid = parse_input(input)
    origin = (500, 0)
    abyss = max(y for x, y in grid)
    ii = 0
    while True:
        ok = sand_trace(origin, grid, abyss=abyss)
        if not ok:
            break
        ii += 1
    return ii


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day14")
    grid = parse_input(input)
    origin = (500, 0)
    floor = 2 + max(y for x, y in grid)
    ii = 0
    while True:
        ok = sand_trace(origin, grid, floor=floor)
        if not ok:
            break
        ii += 1
        if grid.get(origin) is not None:
            break
    return ii


if __name__ == "__main__":
    assert part1() == 755
    assert part2() == 29805
