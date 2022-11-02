import itertools

from _2020.python.utils import load_puzzle_input, profile

puzzle_input = list(map(int, load_puzzle_input("day1").split("\n")))


@profile
def part1():
    for a, b in itertools.combinations(puzzle_input, 2):
        if a + b == 2020:
            return a * b


@profile
def part2():
    for a, b, c in itertools.combinations(puzzle_input, 3):
        if a + b + c == 2020:
            return a * b * c


if __name__ == "__main__":
    part1()
    part2()
