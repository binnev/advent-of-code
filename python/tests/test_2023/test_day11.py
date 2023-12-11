import pytest

from puzzles.y2023.day11 import *

example = """...1......
.......2..
3.........
..........
......4...
.5........
.........6
..........
.......7..
8...9....."""


def test_part1():
    assert part1(example) == 374


def test_parse_input():
    matrix = parse_input(example)
    assert matrix.to_str() == example


def test_detect_empty_rows():
    matrix = parse_input(example)
    empty_rows, empty_cols = detect_empty_rows(matrix)
    assert empty_rows == [3, 7]
    assert empty_cols == [2, 5, 8]


@pytest.mark.parametrize(
    "a, b, expected_dist",
    [
        ("1", "7", 15),
        ("3", "6", 17),
        ("8", "9", 5),
        ("5", "9", 9),
    ],
)
def test_galaxy_distance(a, b, expected_dist):
    matrix = parse_input(example)
    empty_rows, empty_cols = detect_empty_rows(matrix)
    coord_a = next(coord for coord in matrix if matrix[coord] == a)
    coord_b = next(coord for coord in matrix if matrix[coord] == b)
    assert (  # should be symmetrical
        galaxy_distance(coord_a, coord_b, empty_rows, empty_cols)
        == galaxy_distance(coord_b, coord_a, empty_rows, empty_cols)
        == expected_dist
    )
