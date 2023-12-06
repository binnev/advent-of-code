import pytest

from puzzles.y2023 import day6

example1 = """Time:      7  15   30
Distance:  9  40  200"""


def test_part1():
    assert day6.part1(example1) == 288


# def test_part2():
#     assert day6.part2(example1) == ...


@pytest.mark.parametrize(
    "charge_time, total_time, expected_distance",
    [
        (0, 7, 0),
        (1, 7, 6),
        (2, 7, 10),
        (3, 7, 12),
        (4, 7, 12),
        (5, 7, 10),
        (6, 7, 6),
        (7, 7, 0),
    ],
)
def test__calculate_distance(charge_time, total_time, expected_distance):
    distance = day6._calculate_distance(charge_time, total_time)
    assert distance == expected_distance


def test__parse_input():
    assert day6._parse_input(example1) == (
        [7, 15, 30],
        [9, 40, 200],
    )
