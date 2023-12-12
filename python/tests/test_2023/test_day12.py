import pytest
from puzzles.y2023.day12 import *

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_parse_input():
    result = parse_input(example)
    assert result[0] == ("???.###", [1, 1, 3])
    assert result[-1] == ("?###????????", [3, 2, 1])


@pytest.mark.parametrize(
    "springs, numbers, expected",
    [
        ("???.###", [1, 1, 3], ["#.#.###"]),
    ],
)
def test_find_arrangements(springs, numbers, expected):
    assert find_arrangements(springs, numbers) == expected


@pytest.mark.parametrize(
    "springs, number, expected",
    [
        pytest.param(
            "???.###",
            1,
            [(0, 1), (1, 2), (2, 3)],
            id="Should ignore the last group of #s because it is longer than 1",
        ),
        pytest.param(
            "???.###",
            2,
            [(0, 2), (1, 3)],
            id="Should ignore the last group of #s because it is longer than 2",
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
        ("#?.", 1, False),  # too long
        ("?#.", 1, False),  # too long
        (".#.", 1, False),  # not at start
        (".?.", 1, False),  # not at start
    ],
)
def test_is_match(s, length, expected):
    assert is_match(s, length) is expected
