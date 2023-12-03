import pytest

from puzzles.y2023 import day1


@pytest.mark.parametrize(
    "s, expected",
    [
        ("1two", ["1", "two"]),
        ("oneight", ["one", "eight"]),
        ("nineight", ["nine", "eight"]),
        ("twone", ["two", "one"]),
    ],
)
def test_regex_magic(s, expected):
    assert day1._regex_magic(s) == expected
