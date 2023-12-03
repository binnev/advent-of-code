import re

import utils


# @utils.profile
# def part1(input: str):
#     lines = list(map(str.strip, input.splitlines()))
#     rx = re.compile(r"(\d+)+")
#     valid_part_numbers = []
#     for yy, line in enumerate(lines):
#         # find all the numbers in the current line
#         numbers = rx.findall(line)
#         # for each number, look at all the adjacent characters
#         # if any one of those is a symbol, add it to the list of valid part numbers.
#         # otherwise do nothing.
#         for n in numbers:
#             xx = line.index(n)
#             x_min = max(xx - 1, 0)
#             x_max = min(xx + len(n) + 1, len(lines) - 1)
#             y_min = max(yy - 1, 0)
#             y_max = min(yy + 2, len(lines))
#             chars = []
#             for y in range(y_min, y_max):
#                 for x in range(x_min, x_max):
#                     c = lines[y][x]
#                     chars.append(c)
#             for c in chars:
#                 if c not in ".1234567890":
#                     valid_part_numbers.append(int(n))
#
#     return sum(valid_part_numbers)

Coord = tuple[int, int]


def is_symbol(char: str) -> bool:
    return char not in ".1234567890"


def _parse_input(input: str) -> list[str]:
    return [line.strip() for line in input.splitlines()]


def _get_char_neighbours(lines: list[str], xx: int, yy: int) -> list[tuple[str, Coord]]:
    """
    Return a list of chars and their xx,yy coords within the lines list
    """
    neighbours = []
    line = lines[yy]
    x_min = max(0, xx - 1)
    y_min = max(0, yy - 1)
    x_max = min(len(line), xx + 2)  # +2 because we want to include in range
    y_max = min(len(lines), yy + 2)
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            neighbour = lines[y][x]
            neighbours.append((neighbour, (x, y)))
    return neighbours


@utils.profile
def part1(input: str) -> int:
    lines = _parse_input(input)
    valid = []
    for yy, line in enumerate(lines):
        num = ""
        is_valid = False
        line: str
        for xx, char in enumerate(line):
            char: str
            if char.isnumeric():
                num += char
                # check if any surrounding chars are symbols
                neighbours = _get_char_neighbours(lines, xx, yy)
                if any(is_symbol(n) for n, _ in neighbours):
                    is_valid = True

            # if we just finished parsing a number
            else:
                if is_valid:
                    valid.append(int(num))
                num = ""
                is_valid = False

        # if we hit the end of the line while parsing a number
        if num and is_valid:
            valid.append(int(num))
    return sum(valid)


def _find_all_number_coords(lines: list[str]) -> list[list[Coord]]:
    results = []
    for yy, line in enumerate(lines):
        num = []
        for xx, char in enumerate(line):
            if char.isnumeric():
                num.append((xx, yy))  # start a new number
            else:
                if num:
                    results.append(num)  # finish number or not
                num = []
        # when reach end of line, finish number
        if num:
            results.append(num)
    return results


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
    lines = _parse_input(input)
    result = 0
    for yy, line in enumerate(lines):
        for xx, char in enumerate(line):
            if char != "*":
                continue  # consider only gears

            adjacent_numbers = [
                (char, xy) for char, xy in _get_char_neighbours(lines, xx, yy) if char.isnumeric()
            ]
            if len(adjacent_numbers) > 1:
                numbers = _find_numbers(adjacent_numbers, lines)
                product = 1
                for n in numbers:
                    product *= n
                result += product
    return result


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day3")
    assert part1(input) == 527369
    part2(input)
