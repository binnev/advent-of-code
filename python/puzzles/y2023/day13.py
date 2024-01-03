import utils
from utils import SparseMatrix


@utils.profile
def part1(input: str):
    matrices = parse_input(input)
    result = 0
    for matrix in matrices:
        x_left, x_right = find_x_reflection(matrix)
        if None not in (x_left, x_right):
            result += x_left
        else:
            y_top, y_btm = find_y_reflection(matrix)
            result += y_top * 100
    return result


@utils.profile
def part2(input: str):
    matrices = parse_input(input)
    result = 0
    for matrix in matrices:
        y_top, y_btm = find_y_reflection(matrix, allow_diffs=1)
        if None not in (y_top, y_btm):
            result += y_top * 100
        else:
            x_left, x_right = find_x_reflection(matrix, allow_diffs=1)
            result += x_left
    return result


def find_x_reflection(matrix: SparseMatrix, allow_diffs: int = 0) -> tuple[int | None, int | None]:
    x_min, x_max = matrix.get_xlim()
    for xx in range(x_min, x_max):
        xx_left = xx
        xx_right = xx + 1
        if is_x_reflection((xx_left, xx_right), matrix, allow_diffs):
            return (xx_left + 1, xx_right + 1)  # AoC counts 1-based not 0-based
    return None, None


def find_y_reflection(matrix: SparseMatrix, allow_diffs: int = 0) -> tuple[int | None, int | None]:
    y_min, y_max = matrix.get_ylim()
    for yy in range(y_min, y_max):
        yy_left = yy
        yy_right = yy + 1
        if is_y_reflection((yy_left, yy_right), matrix, allow_diffs):
            return (yy_left + 1, yy_right + 1)
    return None, None


def get_x_diffs(
    between: tuple[int, int],
    matrix: SparseMatrix,
    allow_diffs: int = 0,
) -> int:
    xx_left, xx_right = between
    x_min, x_max = matrix.get_xlim()
    y_min, y_max = matrix.get_ylim()
    diffs = 0

    if xx_left < x_min or xx_right > x_max:  # out of bounds
        raise ValueError(
            f"{between} value is out of bounds for matrix with xlim={matrix.get_xlim()}"
        )

    while x_min <= xx_left and xx_right <= x_max:
        for yy in range(y_min, y_max + 1):
            coord_left = (xx_left, yy)
            coord_right = (xx_right, yy)
            value_left = matrix[coord_left]
            value_right = matrix[coord_right]
            if value_left != value_right:
                diffs += 1
                if diffs > allow_diffs:
                    return diffs
        xx_left -= 1
        xx_right += 1

    return diffs


def get_y_diffs(
    between: tuple[int, int],
    matrix: SparseMatrix,
    allow_diffs: int = 0,
) -> int:
    yy_left, yy_right = between  # "left" is upwards (lower y value)
    x_min, x_max = matrix.get_xlim()
    y_min, y_max = matrix.get_ylim()
    diffs = 0

    if yy_left < y_min or yy_right > y_max:
        raise ValueError(
            f"{between} value is out of bounds for matrix with ylim={matrix.get_ylim()}"
        )

    while y_min <= yy_left and yy_right <= y_max:
        for xx in range(x_min, x_max + 1):
            coord_left = (xx, yy_left)
            coord_right = (xx, yy_right)
            value_left = matrix[coord_left]
            value_right = matrix[coord_right]
            if value_left != value_right:
                diffs += 1
                if diffs > allow_diffs:
                    return diffs
        yy_left -= 1
        yy_right += 1
    return diffs


def is_y_reflection(between: tuple[int, int], matrix: SparseMatrix, allow_diffs: int = 0) -> bool:
    return get_y_diffs(between, matrix, allow_diffs) <= allow_diffs


def is_x_reflection(between: tuple[int, int], matrix: SparseMatrix, allow_diffs: int = 0) -> bool:
    return get_x_diffs(between, matrix, allow_diffs) <= allow_diffs


def parse_input(input: str) -> list[SparseMatrix]:
    matrix_strings = list(map(str.strip, input.split("\n\n")))
    matrices = [SparseMatrix.from_str(s) for s in matrix_strings]
    return matrices


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day13")
    part2(input)
