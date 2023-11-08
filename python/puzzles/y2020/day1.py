import itertools

from utils import load_puzzle_input, profile


def process_input(input: str):
    return list(map(int, input.split("\n")))


@profile
def part1(input: str):
    for a, b in itertools.combinations(process_input(input), 2):
        if a + b == 2020:
            return a * b


@profile
def part2(input: str):
    for a, b, c in itertools.combinations(process_input(input), 3):
        if a + b + c == 2020:
            return a * b * c


if __name__ == "__main__":
    input = load_puzzle_input("2020/day1")
    part1(input)
    part2(input)
