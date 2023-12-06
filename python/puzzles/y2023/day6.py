import re

import utils


@utils.profile
def part1(input: str) -> int:
    wins = 1
    times, distances = _parse_input(input)
    for time, distance in zip(times, distances):
        my_distances = [_calculate_distance(charge_time=t, total_time=time) for t in range(time)]
        num_wins = len([d for d in my_distances if d > distance])
        wins *= num_wins
    return wins


@utils.profile
def part2(input: str) -> int:
    ...


def _calculate_distance(charge_time: int, total_time: int) -> int:
    speed = charge_time
    remaining_time = total_time - charge_time
    distance = remaining_time * speed
    return distance


def _parse_input(input: str) -> tuple[list[int], list[int]]:
    rx = re.compile(r"(\d+)")
    lines = input.splitlines()
    times = list(map(int, rx.findall(lines[0])))
    distances = list(map(int, rx.findall(lines[1])))
    return times, distances


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day6")
    part1(input)
