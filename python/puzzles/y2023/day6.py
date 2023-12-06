import re

import utils


@utils.profile
def part1(input: str) -> int:
    wins = 1
    times, distances = _parse_input(input)
    for time, distance in zip(times, distances):
        wins *= _calculate_win_possibilities(time, distance)
    return wins


@utils.profile
def part2(input: str) -> int:
    times, distances = _parse_input(input)
    time = int("".join(map(str, times)))
    distance = int("".join(map(str, distances)))
    return _calculate_win_possibilities(time, distance)


def _calculate_win_possibilities(race_time: int, distance_record: int) -> int:
    my_distances = [
        _calculate_distance(charge_time=t, total_time=race_time) for t in range(race_time)
    ]
    num_wins = len([d for d in my_distances if d > distance_record])
    return num_wins


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
    part2(input)
