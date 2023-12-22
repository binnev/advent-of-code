import pytest

from puzzles.y2023.day21 import *

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

example_after1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

example_after2 = """...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

example_after3 = """...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
..........."""


@pytest.mark.parametrize(
    "steps, expected",
    [
        (1, example_after1),
        (2, example_after2),
        (3, example_after3),
    ],
)
def test_forgetful_bfs_visual(steps, expected):
    matrix, start = parse_input(example)
    reachable = forgetful_bfs({start}, matrix, steps)
    visual = SparseMatrix({**matrix, start: "S", **{coord: "O" for coord in reachable}})
    assert visual.to_str() == expected


def test_forgetful_bfs_part1():
    matrix, start = parse_input(example)
    reachable = forgetful_bfs({start}, matrix, 6)
    assert len(reachable) == 16
