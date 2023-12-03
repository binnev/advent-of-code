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


def is_symbol(char: str) -> bool:
    return char not in ".1234567890"


@utils.profile
def part1(input: str) -> int:
    lines: list[str] = [line.strip() for line in input.splitlines()]
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
                x_min = max(0, xx - 1)
                y_min = max(0, yy - 1)
                x_max = min(len(line), xx + 2)  # +2 because we want to include in range
                y_max = min(len(lines), yy + 2)
                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        neighbour = lines[y][x]
                        if is_symbol(neighbour):
                            is_valid = True
                            break

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


@utils.profile
def part2(input: str):
    ...


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day3")
    assert part1(input) == 527369
