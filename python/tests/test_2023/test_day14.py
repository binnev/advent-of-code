import pytest

from puzzles.y2023.day14 import *

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

example2 = """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""

example_after_1_spin_cycles = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

example_after_2_spin_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""

example_after_3_spin_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""

example_rotation = """abc
ABC
123"""

example_rotation_expected = """1Aa
2Bb
3Cc"""


@pytest.fixture
def example_matrix():
    return parse_input(example)


def test_part1():
    assert part1(example) == 136


#
def test_part2():
    assert part2(example) == 64


def test_parse_input(example_matrix):
    assert example_matrix.to_str() == example


@pytest.mark.parametrize(
    "coord, expected",
    [
        ((0, 0), (0, 0)),  # move not possible
        ((0, 1), (0, 1)),  # move not possible
        ((2, 6), (2, 6)),  # move not possible
        ((1, 3), (1, 0)),
    ],
)
def test_move_rock_north(coord, expected, example_matrix):
    assert move_rock_north(coord, example_matrix) == expected


def test_slide_north(example_matrix):
    slide_north(example_matrix)
    assert example_matrix.to_str() == example2


def test_rotate_string_clockwise():
    assert rotate_string_clockwise(example_rotation) == example_rotation_expected
    matrix = parse_input(example_rotation)
    assert rotate_clockwise(matrix).to_str() == example_rotation_expected


def test_spin_cycle(example_matrix):
    matrix = example_matrix
    assert matrix.to_str() == example
    matrix = spin_cycle(matrix)
    assert matrix.to_str() == example_after_1_spin_cycles
    matrix = spin_cycle(matrix)
    assert matrix.to_str() == example_after_2_spin_cycles
    matrix = spin_cycle(matrix)
    assert matrix.to_str() == example_after_3_spin_cycles


def test_get_loop_length():
    start, length = get_loop_length([0, 1, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3])
    assert start == 2
    assert length == 4
    start, length = get_loop_length([0, 1, 2, 1, 2])
    assert start == 1
    assert length == 2
    start, length = get_loop_length("abcdefdef")
    assert start == 3
    assert length == 3


@pytest.mark.parametrize(
    "cycles, expected",
    [
        (4, 3),
        (8, 3),
        (12, 3),
        (15, 2),
        (16, 3),
        (17, 4),
    ],
)
def test_get_final_value(cycles, expected):
    #                ----------  ----------  ----------
    #          1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
    history = [0, 1, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3]
    assert get_final_value(history, cycles) == expected
