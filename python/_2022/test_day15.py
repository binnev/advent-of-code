import pytest

from python._2022.day15 import Range


@pytest.mark.parametrize(
    "range1, range2, expected_result",
    [
        ((0, 2), (1, 3), True),
        ((0, 1), (2, 3), False),
        ((0, 1), (3, 2), False),
        ((0, 1), (3, 4), False),
        ((0, 1), (1, 3), True),
        ((2, 3), (0, 2), True),
        ((0, 3), (1, 2), True),
        ((1, 2), (0, 3), True),
        ((0, 1), (0, 1), True),
        ((0, 1), (1, 0), True),
    ],
)
def test_range_intersects(range1, range2, expected_result):
    range1 = Range(*range1)
    range2 = Range(*range2)
    assert range1.intersects(range2) == expected_result
