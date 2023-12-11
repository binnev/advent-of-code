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

    input = utils.load_puzzle_input("2023/day9")
    sequences = parse_input(input)
    assert sequences[0][0] == 17
    assert sequences[0][-1] == 137
    assert sequences[5][0] == 2
    assert sequences[5][1] == -2
    assert sequences[-1][0] == 14
    assert sequences[-1][-1] == 549375
    assert sequences[-3][0] == -5
    assert sequences[-3][-1] == 13645596


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
        ([0, 1, 1, 0], -2),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
        ([1, -4, -9, -14, -19, -24, -29, -34, -39, -44], -49),
        (
            [
                2,
                2,
                6,
                33,
                127,
                380,
                967,
                2193,
                4552,
                8798,
                16028,
                27777,
                46125,
                73816,
                114389,
                172321,
                253182,
                363802,
                512450,
                709025,
            ],
            965259,
        ),
    ],
)
def test_predict_next_value(input, expected):
    assert predict_next_value(input) == expected


@pytest.mark.parametrize(
    "input",
    parse_input(utils.load_puzzle_input("2023/day9")),
)
def test_predict_next_value2(input):
    last = input[-1]
    input = input[:-1]
    assert predict_next_value(input) == last
