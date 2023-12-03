import utils
from utils import Coord, SparseMatrix

NumberCoords = tuple[Coord, ...]


def is_symbol(char: str) -> bool:
    return char not in ".1234567890"


def _parse_input(input: str) -> list[str]:
    return [line.strip() for line in input.splitlines()]


def _parse_input_matrix(input: str) -> SparseMatrix:
    """
    How could I forget: SparseMatrix, the godlike data structure that reduces AoC difficulty by
    an order of magnitude at least.
    """
    lines = _parse_input(input)
    result = SparseMatrix()
    for yy, line in enumerate(lines):
        for xx, char in enumerate(line):
            result[(xx, yy)] = char
    return result


def _get_char_neighbours(matrix: SparseMatrix, xx: int, yy: int) -> SparseMatrix:
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


@utils.profile
def part1(input: str) -> int:
    matrix = _parse_input_matrix(input)
    number_coords = _find_all_number_coords(_parse_input(input))

    valid = []
    for coords, num in number_coords.items():
        # gather all the characters adjacent to the number
        neighbours = SparseMatrix()
        for xx, yy in coords:
            neighbours.update(_get_char_neighbours(matrix, xx, yy))

        if any(is_symbol(char) for _, char in neighbours.items()):
            valid.append(num)
    return sum(valid)


def _find_numbers(numbers: list[tuple[str, Coord]], lines: list[str]) -> set[int]:
    """Given the coords of digits, get the full numbers"""
    all_number_coords = _find_all_number_coords(lines)
    integers = set()
    for str, coord in numbers:
        for number_coords in all_number_coords:
            if coord in number_coords:
                number = "".join(lines[y][x] for x, y in number_coords)
                integers.add(int(number))
    return integers


@utils.profile
def part2(input: str):
    matrix = _parse_input_matrix(input)
    number_coords = _find_all_number_coords(_parse_input(input))

    result = 0
    for (xx, yy), char in matrix.items():
        if char != "*":
            continue  # consider only gears

        neighbours = _get_char_neighbours(matrix, xx, yy)
        neighbouring_numbers_coords = set()
        for coord in neighbours:
            for coords, number in number_coords.items():
                if coord in coords:
                    neighbouring_numbers_coords.add(coords)

        if len(neighbouring_numbers_coords) > 1:
            product = 1
            for coords in neighbouring_numbers_coords:
                number = number_coords[coords]
                product *= number
            result += product

    return result


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day3")
    assert part1(input) == 527369
    assert part2(input) == 73074886
