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


@pytest.fixture
def example_matrix():
    return parse_input(example)


def test_part1():
    assert part1(example) == 136


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


debug = """OOOO.#....
O...#....#
O...O##..O
...#......
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def test_sanity():
    matrix = parse_input(debug)
    assert move_rock_north((1, 4), matrix) == (1, 1)


def test_slide_north(example_matrix):
    slide_north(example_matrix)
    assert example_matrix.to_str() == example2


def test_sanity():
    assert list(range(0, 4)) == [0, 1, 2, 3]
    assert list(reversed(range(0, 4))) == [3, 2, 1, 0]
