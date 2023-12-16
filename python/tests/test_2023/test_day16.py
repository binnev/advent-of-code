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

example_instant_reflect = r"""\.
..
.."""


def test_part1():
    assert part1(example) == 46


def test_part2():
    assert part2(example) == 51


def test_parse_input():
    matrix = parse_input(example)
    assert matrix.to_str() == example


def test_trace_beam_instant():
    matrix = parse_input(example_instant_reflect)
    assert trace_beam(matrix) == 3  # should be reflected vertically immediately
