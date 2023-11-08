import itertools

from utils import load_puzzle_input, profile


def process_input(raw: str):
    return list(map(int, raw.split("\n")))


@profile
def part1(raw: str):
    for a, b in itertools.combinations(process_input(raw), 2):
        if a + b == 2020:
            return a * b


@profile
def part2(raw: str):
    for a, b, c in itertools.combinations(process_input(raw), 3):
        if a + b + c == 2020:
            return a * b * c


if __name__ == "__main__":
    raw = load_puzzle_input("2020/day1")
    part1(raw)
    part2(raw)
