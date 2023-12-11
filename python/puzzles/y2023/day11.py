import itertools

import utils
from utils import SparseMatrix, Coord

EMPTY = "."


@utils.profile
def part1(input: str):
    matrix, empty_rows, empty_cols = parse_input(input)
    return calculate_total_distance(matrix, empty_rows, empty_cols, empty_multiplier=2)


@utils.profile
def part2(input: str):
    matrix, empty_rows, empty_cols = parse_input(input)
    return calculate_total_distance(matrix, empty_rows, empty_cols, empty_multiplier=1_000_000)


def calculate_total_distance(
    matrix: SparseMatrix,
    empty_rows: set[int],
    empty_cols: set[int],
    empty_multiplier: int,
) -> int:
    return sum(
        galaxy_distance(galaxy1, galaxy2, empty_rows, empty_cols, empty_multiplier)
        for galaxy1, galaxy2 in itertools.combinations(matrix, 2)
    )


def galaxy_distance(
    galaxy1: Coord,
    galaxy2: Coord,
    empty_rows: set[int],
    empty_cols: set[int],
    empty_multiplier: int,
) -> int:
    """
    1. taxicab distance
    2. see how many empty rows are crossed, add that
    """
    x1, y1 = galaxy1
    x2, y2 = galaxy2
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    x_dist = x_max - x_min
    y_dist = y_max - y_min
    empty_rows_crossed = sum(1 for row in empty_rows if y_min < row < y_max)
    empty_cols_crossed = sum(1 for col in empty_cols if x_min < col < x_max)
    # -1 because we already crossed each empty row/col once when we calculated x_dist and y_dist
    total_distance = (
        x_dist
        + empty_cols_crossed * (empty_multiplier - 1)
        + y_dist
        + empty_rows_crossed * (empty_multiplier - 1)
    )
    return total_distance


def parse_input(input: str) -> tuple[SparseMatrix, set[int], set[int]]:
    empty_rows = set()
    empty_cols = set()
    matrix = SparseMatrix()
    for yy, line in enumerate(input.splitlines()):
        empty_line = True
        empty_xx = set()

        for xx, char in enumerate(line):
            if char != EMPTY:
                coord = (xx, yy)
                matrix[coord] = char
                empty_line = False
            else:
                empty_xx.add(xx)

        if yy == 0:
            empty_cols = empty_xx
        else:
            empty_cols &= empty_xx

        if empty_line:
            empty_rows.add(yy)
    return matrix, empty_rows, empty_cols
