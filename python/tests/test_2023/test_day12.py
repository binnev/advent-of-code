import pytest
from puzzles.y2023.day12 import *

# pytestmark = pytest.mark.timeout(3)

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@pytest.mark.parametrize(
    "line, numbers, expected",
    [
        ("???.###", [1, 1, 3], ["#.#.###"]),
        (
            ".??..??...?##.",
            [1, 1, 3],
            [
                ".#...#....###.",
                ".#....#...###.",
                "..#..#....###.",
                "..#...#...###.",
            ],
        ),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], [".#.###.#.######"]),
        ("????.#...#...", [4, 1, 1], ["####.#...#..."]),
        (
            "????.######..#####.",
            [1, 6, 5],
            [
                "#....######..#####.",
                ".#...######..#####.",
                "..#..######..#####.",
                "...#.######..#####.",
            ],
        ),
        (
            "?###????????",
            [3, 2, 1],
            [
                ".###.##.#...",
                ".###.##..#..",
                ".###.##...#.",
                ".###.##....#",
                ".###..##.#..",
                ".###..##..#.",
                ".###..##...#",
                ".###...##.#.",
                ".###...##..#",
                ".###....##.#",
            ],
        ),
    ],
)
@pytest.mark.parametrize(
    "func",
    [
        brute,
        elegant,
    ],
)
def test_brute_elegant(func, line, numbers, expected):
    result = func(line, numbers)
    assert result == expected


def test_part1():
    assert part1(example) == 21


# def test_part2():
#     assert part2(example) == 525152


def test_parse_input():
    result = parse_input(example)
    assert result[0] == ("???.###", [1, 1, 3])
    assert result[-1] == ("?###????????", [3, 2, 1])


@pytest.mark.parametrize(
    "springs, numbers, expected",
    [
        (".#", [1], (".#?.#?.#?.#?.#", [1, 1, 1, 1, 1])),
        (
            "???.###",
            [1, 1, 3],
            (
                "???.###????.###????.###????.###????.###",
                [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3],
            ),
        ),
    ],
)
def test_unfold(springs, numbers, expected):
    assert unfold(springs, numbers) == expected


@pytest.mark.parametrize(
    "s, numbers, expected",
    [
        ("", [1], False),
        ("#", [1], True),
        ("##", [2], True),
        ("##", [1], False),
        ("#", [2], False),
        ("#.#", [2], False),
        ("#.#", [1, 1], True),
        ("#.#", [1, 2], False),
        ("#..##.....###", [1, 2, 3], True),
    ],
)
def test_satisfies_pattern(s, numbers, expected):
    assert satisfies_pattern(s, numbers) == expected
