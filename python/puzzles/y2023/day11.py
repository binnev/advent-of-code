import itertools

import utils
from utils import SparseMatrix, Coord


@utils.profile
def part1(input: str):
    matrix = parse_input(input)
    empty_rows, empty_cols = detect_empty_rows(matrix)
    return sum(
        galaxy_distance(galaxy1, galaxy2, empty_rows, empty_cols, empty_multiplier=2)
        for galaxy1, galaxy2 in itertools.combinations(matrix, 2)
    )


@utils.profile
def part2(input: str):
    matrix = parse_input(input)
    empty_rows, empty_cols = detect_empty_rows(matrix)
    return sum(
        galaxy_distance(galaxy1, galaxy2, empty_rows, empty_cols, empty_multiplier=1_000_000)
        for galaxy1, galaxy2 in itertools.combinations(matrix, 2)
    )


def galaxy_distance(
    galaxy1: Coord,
    galaxy2: Coord,
    empty_rows: list[int],
    empty_cols: list[int],
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
    total_distance = (
        x_dist
        + empty_cols_crossed * (empty_multiplier - 1)
        + y_dist
        + empty_rows_crossed * (empty_multiplier - 1)
    )
    return total_distance


def detect_empty_rows(matrix: SparseMatrix) -> tuple[list[int], list[int]]:
    empty_rows = []
    empty_cols = []
    xmin, xmax = matrix.get_xlim()
    ymin, ymax = matrix.get_ylim()
    for yy in range(ymin, ymax + 1):
        row = {matrix[(xx, yy)] for xx in range(xmin, xmax + 1) if (xx, yy) in matrix}
        if not row:
            empty_rows.append(yy)
    for xx in range(xmin, xmax + 1):
        col = {matrix[(xx, yy)] for yy in range(ymin, ymax + 1) if (xx, yy) in matrix}
        if not col:
            empty_cols.append(xx)
    return empty_rows, empty_cols


def parse_input(input: str) -> SparseMatrix:
    matrix = SparseMatrix()
    for yy, line in enumerate(input.splitlines()):
        for xx, char in enumerate(line):
            if char != ".":
                coord = (xx, yy)
                matrix[coord] = char
    return matrix
