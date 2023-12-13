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
    ...


def find_x_reflection(matrix: SparseMatrix) -> tuple[int | None, int | None]:
    x_min, x_max = matrix.get_xlim()
    for xx in range(x_min, x_max + 1):
        # reflection line
        xx_left = xx
        xx_right = xx + 1
        if is_x_reflection((xx_left, xx_right), matrix):
            return (xx_left + 1, xx_right + 1)  # AoC counts 1-based not 0-based
    return None, None


def find_y_reflection(matrix: SparseMatrix) -> tuple[int | None, int | None]:
    y_min, y_max = matrix.get_ylim()
    for yy in range(y_min, y_max + 1):
        yy_top = yy
        yy_btm = yy + 1
        if is_y_reflection((yy_top, yy_btm), matrix):
            return (yy_top + 1, yy_btm + 1)
    return None, None


def is_x_reflection(between: tuple[int, int], matrix: SparseMatrix) -> bool:
    xx_left, xx_right = between
    x_min, x_max = matrix.get_xlim()
    y_min, y_max = matrix.get_ylim()

    if xx_left < x_min or xx_right > x_max:  # out of bounds
        return False

    while x_min <= xx_left and xx_right <= x_max:
        for yy in range(y_min, y_max + 1):
            coord_left = (xx_left, yy)
            coord_right = (xx_right, yy)
            value_left = matrix[coord_left]
            value_right = matrix[coord_right]
            if value_left != value_right:
                return False  # fail early
        xx_left -= 1
        xx_right += 1

    return True  # all checks passed


def is_y_reflection(between: tuple[int, int], matrix: SparseMatrix) -> bool:
    yy_top, yy_btm = between
    x_min, x_max = matrix.get_xlim()
    y_min, y_max = matrix.get_ylim()

    if yy_top < y_min or yy_btm > y_max:  # out of bounds
        return False

    while y_min <= yy_top and yy_btm <= y_max:  # remember y is positive downwards
        for xx in range(x_min, x_max + 1):
            coord_top = (xx, yy_top)
            coord_btm = (xx, yy_btm)
            value_top = matrix[coord_top]
            value_btm = matrix[coord_btm]
            if value_top != value_btm:
                return False
        yy_top -= 1
        yy_btm += 1
    return True


def parse_input(input: str) -> list[SparseMatrix]:
    matrix_strings = list(map(str.strip, input.split("\n\n")))
    matrices = [SparseMatrix.from_str(s) for s in matrix_strings]
    return matrices


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day13")
    print(input)
