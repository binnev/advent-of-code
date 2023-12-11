import pytest
from puzzles.y2023.day9 import *

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_part1():
    assert part1(example) == 114


def test_parse_input():
    assert parse_input(example) == [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [0, 3, 6, 9, 12, 15],
            [3, 3, 3, 3, 3],
        ),
        (
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0],
        ),
        (
            [10, 13, 16, 21, 30, 45],
            [3, 3, 5, 9, 15],
        ),
        (
            [1, -4, -9, -14, -19, -24, -29, -34, -39, -44],
            [-5, -5, -5, -5, -5, -5, -5, -5, -5],
        ),
    ],
)
def test_get_differential(input, expected):
    assert get_differential(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
        (
            [
                1,
                -4,
                -9,
                -14,
                -19,
                -24,
                -29,
                -34,
                -39,
                -44,
                -49,
                -54,
                -59,
                -64,
                -69,
                -74,
                -79,
                -84,
                -89,
                -94,
                -99,
            ],
            -104,
        ),
    ],
)
def test_predict_next_value(input, expected):
    assert predict_next_value(input) == expected
