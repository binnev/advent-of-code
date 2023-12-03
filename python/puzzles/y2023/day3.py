from functools import reduce
from operator import mul

import utils
from utils import Coord, SparseMatrix

NumberCoords = tuple[Coord, ...]


def _is_symbol(char: str) -> bool:
    return char not in ".1234567890"


def _parse_input(input: str) -> list[str]:
    return [line.strip() for line in input.splitlines()]


def _parse_input_matrix(input: str) -> SparseMatrix:
    """
    How could I forget: SparseMatrix, the godlike data structure that reduces
    AoC difficulty by an order of magnitude at least.
    """
    lines = _parse_input(input)
    result = SparseMatrix()
    for yy, line in enumerate(lines):
        for xx, char in enumerate(line):
            result[(xx, yy)] = char
    return result


def _get_neighbours(matrix: SparseMatrix, xx: int, yy: int) -> SparseMatrix:
    neighbour_coords = (
        (xx - 1, yy - 1),
        (xx - 1, yy),
        (xx - 1, yy + 1),
        (xx, yy - 1),
        (xx, yy + 1),
        (xx + 1, yy - 1),
        (xx + 1, yy),
        (xx + 1, yy + 1),
    )
    neighbours = {coord: matrix[coord] for coord in neighbour_coords if coord in matrix}
    return SparseMatrix(neighbours)


def _find_all_number_coords(lines: list[str]) -> dict[NumberCoords, int]:
    results = {}
    for yy, line in enumerate(lines):
        coords = []
        num_str = ""
        for xx, char in enumerate(line):
            if char.isnumeric():
                coords.append((xx, yy))  # start a new number
                num_str += char
            else:
                if coords:
                    results[tuple(coords)] = int(num_str)
                coords = []
                num_str = ""
        # when reach end of line, finish number
        if coords:
            results[tuple(coords)] = int(num_str)

    return results


def _get_full_number_coords(
    coord: Coord,
    all_number_coords: dict[NumberCoords, int],
) -> tuple[NumberCoords, int]:
    """
    Given a char + coord, find the coordinates of the full number they belong to,
    if it exists.
    """
    for coords, number in all_number_coords.items():
        if coord in coords:
            return coords, number
    return (), 0  # if no number found


@utils.profile
def part1(input: str) -> int:
    """
    Iterate over all the numbers, and check their surroundings for symbols
    """
    matrix = _parse_input_matrix(input)
    number_coords = _find_all_number_coords(_parse_input(input))

    valid = []
    for coords, num in number_coords.items():
        # gather all the characters adjacent to the number
        neighbours = SparseMatrix()
        for xx, yy in coords:
            neighbours.update(_get_neighbours(matrix, xx, yy))

        if any(_is_symbol(char) for _, char in neighbours.items()):
            valid.append(num)
    return sum(valid)


@utils.profile
def part2(input: str):
    """
    Iterate over the gears, and check their surroundings for numbers
    """
    matrix = _parse_input_matrix(input)
    all_numbers: dict[NumberCoords, int] = _find_all_number_coords(_parse_input(input))

    result = 0
    gears = {coord: char for coord, char in matrix.items() if char == "*"}
    for (xx, yy), char in gears.items():
        # Start by finding all neighbouring digits.
        # But these could be part of the same number, so we need to do some clever stuff.
        # Once we have all the neighbouring numbers, we can compute the product if there's more
        # than 1.
        neighbours = _get_neighbours(matrix, xx, yy)
        neighbouring_digits = {coord for coord, char in neighbours.items() if char.isdigit()}
        neighbouring_numbers: dict[NumberCoords, int] = dict(
            _get_full_number_coords(coord, all_numbers) for coord in neighbouring_digits
        )
        if len(neighbouring_numbers) > 1:
            product = reduce(mul, neighbouring_numbers.values())
            result += product

    return result


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day3")
    assert part1(input) == 527369
    assert part2(input) == 73074886
