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


my_example = """
#############
#...........#
#.#########.#
#S#########.#
#...#######.#
###.#######.#
#...........#
#############
"""
my_example = """
.......
.......
...S...
.......
.......
"""


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


# @pytest.mark.parametrize(
#     "steps, expected",
#     [
#         (6, 16),
#         (10, 50),
#         (50, 1594),
#         (100, 6536),
#         # (500, 167004),
#         # (1000, 668697),
#         # (5000, 16733044),
#         # (26501365, ...),  # too slow
#     ],
# )
# def test_forgetful_bfs_infinite(steps, expected):
#     matrix, start = parse_input(example)
#     reachable = forgetful_bfs_summary({start}, matrix, steps)
#     assert reachable == expected


@pytest.mark.parametrize(
    "steps, expected",
    [
        # (1, 2),
        (2, 4),
        (3, 6),
        (4, 9),
        (5, 13),
        (6, 16),
    ],
)
@pytest.mark.parametrize(
    "algo",
    [
        # forgetful_bfs_summary,
        hopeful_maths,
        bfs_once,
    ],
)
def test_finite_example(algo, steps, expected):
    matrix, start = parse_input(example)
    reachable = algo({start}, matrix, steps)
    assert reachable == expected


# @pytest.mark.parametrize(
#     "steps, expected",
#     [
#         (50, 2222),
#         (75, 4846),
#         (100, 6714),
#         (200, 7521),
#     ],
# )
@pytest.mark.parametrize(
    "algo",
    [
        forgetful_bfs_summary,
        hopeful_maths,
        bfs_once,
    ],
)
def test_finite_input_algos(algo):
    steps = [50, 75, 100, 200]
    expected = [2222, 4846, 6714, 7521]
    matrix, start = parse_input(utils.load_puzzle_input("2023/day21"))
    results = [algo({start}, matrix, s) for s in steps]
    assert results == expected


def test_diamond_expands_forever():
    matrix, start = parse_input(my_example)
    frontier = {start}
    steps = 10
    for _ in range(steps):
        print("----------------")
        frontier = forgetful_bfs(frontier, matrix, 1)
        visual = SparseMatrix({**matrix, start: "S", **{coord: "O" for coord in frontier}})
        visual.print()


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ((5, 5), (6, 5), 1),
        ((6, 5), (5, 5), 1),
        ((0, 0), (0, 1), 1),
        ((0, 0), (0, -1), 1),
    ],
)
def test_taxicab_dist(a, b, expected):
    assert taxicab_dist(a, b) == expected
