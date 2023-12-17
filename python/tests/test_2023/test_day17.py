import pytest

from puzzles.y2023.day17 import *

example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

small3 = """111
222
333"""

small4 = """1111
2222
3333
4444"""

small5 = """11111
22222
33333
44444
55555"""


@pytest.mark.parametrize(
    "input, expected",
    [
        (small3, 8),
        (small4, 4 + 2 + 3 + 4),
        (small5, 1 + 1 + 1 + 1 + 2 + 2 + 3 + 4 + 5),
        # (example, 102),
    ],
)
def test_part1(input, expected):
    assert part1(input) == expected


def test_get_neighbour_generator():
    matrix = parse_input(example)
    get_neighbours = get_neighbour_generator(matrix)

    assert get_neighbours((0, 0)) == [
        (Direction.RIGHT, (1, 0)),
        (Direction.DOWN, (0, 1)),
    ]

    assert get_neighbours((420, 420)) == []  # because out of bounds
