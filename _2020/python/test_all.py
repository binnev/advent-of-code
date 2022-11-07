import pytest

from _2020.python import day1, day2


@pytest.mark.parametrize(
    "module, func, expected_output",
    [
        (day1, "part1", 145875),
        (day1, "part2", 69596112),
        (day2, "part1", 628),
        (day2, "part2", 705),
    ],
)
def test(module, func, expected_output):
    func = getattr(module, func)
    assert func() == expected_output
