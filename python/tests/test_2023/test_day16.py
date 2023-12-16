from puzzles.y2023.day16 import *

example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def test_part1():
    assert part1(example) == 46


def test_parse_input():
    matrix = parse_input(example)
    assert matrix.to_str() == example
