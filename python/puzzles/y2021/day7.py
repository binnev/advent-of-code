import numpy

import utils


def init(raw: str):
    return list(map(int, raw.split(",")))


@utils.profile
def part1(raw: str):
    crabs = init(raw)
    min_x = min(crabs)
    max_x = max(crabs)
    results = {}
    for x in range(min_x, max_x):
        cost = sum(abs(crab - x) for crab in crabs)
        results[x] = cost
    return min(results.values())


def cost(x, desired_x):
    """sum of natural numbers"""
    num_steps = abs(desired_x - x)
    return int(num_steps * (num_steps + 1) / 2)


@utils.profile
def part2(raw: str):
    crabs = init(raw)
    average = int(numpy.mean(crabs))
    min_x = average - 10
    max_x = average + 10
    results = {x: sum(cost(crab, x) for crab in crabs) for x in range(min_x, max_x)}
    return min(results.values())


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day7")
    assert part1(raw) == 333755
    assert part2(raw) == 94017638
