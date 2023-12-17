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

small6 = """111111
222222
333333
444444
555555
666666"""

small4_diagonal = """
1555
1155
5115
5511
"""

small6_nonlinear = """
188111
111181
888881
888111
888188
888111
"""

small6_diagonal = """
155555
115555
511555
551155
555115
555511
"""


@pytest.mark.parametrize(
    "input, expected",
    [
        (small3, 1 + 1 + 2 + 3),
        (small4, 1 + 1 + 1 + 2 + 3 + 4),
        (small5, 1 + 1 + 1 + 2 + 2 + 3 + 4 + 5),
        (small6, 1 + 1 + 1 + 2 + 2 + 3 + 3 + 4 + 5 + 6),
        (small4_diagonal, 6),
        (small6_diagonal, 10),
        (small6_nonlinear, 16),
        (example, 102),
    ],
)
def test_part1(input, expected):
    assert part1(input) == expected
