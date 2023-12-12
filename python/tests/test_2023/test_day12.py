import pytest
from puzzles.y2023.day12 import *

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_part1():
    assert part1(example) == 21


def test_parse_input():
    result = parse_input(example)
    assert result[0] == ("???.###", [1, 1, 3])
    assert result[-1] == ("?###????????", [3, 2, 1])


@pytest.mark.parametrize(
    "springs, numbers, expected",
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
def test_find_arrangements(springs, numbers, expected):
    # assert find_arrangements(springs, numbers) == expected
    assert brute(springs, numbers) == expected


@pytest.mark.parametrize(
    "springs, number, expected",
    [
        pytest.param(
            "",
            1,
            [],
            id="Empty string -> no possible places",
        ),
        pytest.param(
            "....",
            1,
            [],
            id="No #? characters -> no possible places",
        ),
        pytest.param(
            "???.#?#",
            1,
            [(0, 1), (1, 2), (2, 3)],
            id="Should ignore the last ? because it will be longer than 1",
        ),
        pytest.param(
            "???.#?#",
            2,
            [(0, 2), (1, 3)],
            id="Should ignore the last ? because it will be longer than 2",
        ),
        pytest.param(
            "???.#?#",
            3,
            [(0, 3)],
            id="Should ignore the last group of #s because it is longer than 3",
        ),
        pytest.param(
            "?###?",
            3,
            [(1, 4)],
            id=(
                "Should only return the middle group of #s because any other "
                "combination would result in a group of more than 3 long."
            ),
        ),
        pytest.param(
            "#??.###",
            1,
            [(2, 3)],
            id="Shouldn't match the hash at the beginning -- that's already set",
        ),
    ],
)
def test_get_possible_places(springs, number, expected):
    assert get_possible_places(springs, number) == expected


@pytest.mark.parametrize(
    "s, length, expected",
    [
        ("", 1, False),
        ("#", 1, True),
        ("?", 1, True),
        ("...", 1, False),
        ("?..", 1, True),
        ("#..", 1, True),
        ("#?.", 1, True),  # trailing ? might not be a #
        ("?#.", 1, False),  # too long; with trailing # it will be 2 long
        ("?#.", 2, True),  # ?# together make 2
        (".#.", 1, False),  # not at start
        (".?.", 1, False),  # not at start
        ("??#?..", 3, True),  # trailing ? might not be a #
        ("?#?..", 3, True),
        ("?##..", 3, True),
        ("??#..", 3, True),
        ("?##..", 2, False),
        ("??#..", 2, False),
        ("#??..", 2, True),
        ("#?##.", 3, False),  # if the ? is a # then group will be 4 long
        ("???#.", 3, False),
    ],
)
def test_is_match(s, length, expected):
    assert is_match(s, length) is expected


@pytest.mark.parametrize(
    "s, m, expected",
    [
        ("01234", (0, 1), "#1234"),
        ("01234", (0, 2), "##234"),
        ("01234", (1, 2), "0#234"),
        ("01234", (1, 3), "0##34"),
    ],
)
def test_substitute_hashes(s, m, expected):
    assert substitute_hashes(s, m) == expected


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
