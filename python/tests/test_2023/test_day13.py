from puzzles.y2023.day13 import *

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_part1():
    assert part1(example) == 405


def test_find_x_reflection():
    matrix = parse_input(example)[0]
    assert find_x_reflection(matrix) == (5, 6)

    matrix = parse_input(example)[1]
    assert find_x_reflection(matrix) == (None, None)


def test_find_y_reflection():
    matrix = parse_input(example)[0]
    assert find_y_reflection(matrix) == (None, None)

    matrix = parse_input(example)[1]
    assert find_y_reflection(matrix) == (4, 5)


def test_parse_input():
    parsed = parse_input(example)
    assert len(parsed) == 2
    assert isinstance(parsed[0], SparseMatrix)
    assert isinstance(parsed[1], SparseMatrix)
