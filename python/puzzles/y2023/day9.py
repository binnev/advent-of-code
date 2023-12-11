import re

import utils


@utils.profile
def part1(input: str):
    sequences = parse_input(input)
    return sum(predict_next_value(seq) for seq in sequences)


@utils.profile
def part2(input: str):
    ...


def parse_input(input: str) -> list[list[int]]:
    result = []
    for line in input.splitlines():
        result.append(list(map(int, re.findall(r"\d+", line))))
    return result


def get_differential(seq: list[int]) -> list[int]:
    return [current - seq[ii - 1] for ii, current in enumerate(seq[1:], start=1)]


def predict_next_value(seq: list[int]) -> int:
    diffs = []
    diff = seq
    while any(diff):
        diffs.append(diff)
        diff = get_differential(diff)
    return sum(diff[-1] for diff in diffs)


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day9")
    print(input)
    part1(input)
