import pytest

from . import day1, day2


@pytest.mark.parametrize(
    "func, input, expected_output",
    [
        (day1.part1, day1.raw, 145875),
        (day1.part2, day1.raw, 69596112),
        (day2.part1, day2.raw, 628),
        (day2.part2, day2.raw, 705),
    ],
)
def test(func, input, expected_output):
    assert func(input) == expected_output
