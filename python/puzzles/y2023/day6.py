import math
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
    """
    We can find where the distance function intersects the record distance, and structure it as a
    quadratic equation:
    -c**2 + c*t - r = 0
    where c = charge time
          t = total race time
          r = record distance

    solving for c gives us the two roots.
    """
    times, distances = _parse_input(input)
    time = int("".join(map(str, times)))
    distance = int("".join(map(str, distances)))

    roots = _solve_quadratic(a=-1, b=time, c=-distance)
    start = math.ceil(min(roots))
    end = math.floor(max(roots))
    return end - start + 1


def _calculate_win_possibilities(race_time: int, distance_record: int) -> int:
    my_distances = [
        _calculate_distance(charge_time=t, total_time=race_time) for t in range(race_time)
    ]
    num_wins = len([d for d in my_distances if d > distance_record])
    return num_wins


def _calculate_distance(charge_time: int, total_time: int) -> int:
    """
    speed = charge_time
    remaining_time = total_time - charge_time
    distance = remaining_time * speed
    distance = (total_time - charge_time) * charge_time
    """
    return (total_time - charge_time) * charge_time


def _solve_quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    neg = (-b - (math.sqrt(b**2 - 4 * a * c))) / (2 * a)
    pos = (-b + (math.sqrt(b**2 - 4 * a * c))) / (2 * a)
    return neg, pos


def _parse_input(input: str) -> tuple[list[int], list[int]]:
    rx = re.compile(r"(\d+)")
    lines = input.splitlines()
    times = list(map(int, rx.findall(lines[0])))
    distances = list(map(int, rx.findall(lines[1])))
    return times, distances


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day6")
    part2(input)
