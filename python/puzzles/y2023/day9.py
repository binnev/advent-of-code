import re

import utils


@utils.profile
def part1(input: str):
    sequences = parse_input(input)
    return sum(map(predict_next_value, sequences))


@utils.profile
def part2(input: str):
    ...


def parse_input(input: str) -> list[list[int]]:
    result = []
    for line in input.splitlines():
        result.append(list(map(int, re.findall(r"[\d-]+", line))))
    return result


def get_differential(seq: list[int]) -> list[int]:
    return [current - seq[ii - 1] for ii, current in enumerate(seq[1:], start=1)]


def predict_next_value(seq: list[int]) -> int | None:
    """
    The next value is calculated by summing the last value of every differential.
    Once we realise this, we don't actually have to hold on to all the diffs.
    Return None if the sequence doesn't converge.
    """
    next_value = 0
    diff = seq
    history = []
    while any(diff):
        next_value += diff[-1]
        history.append(diff)
        diff = get_differential(diff)

    if len(diff) == 0:
        raise ValueError(f"Sequence didn't converge: {seq}")
    return next_value


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day9")
    part1(input)
