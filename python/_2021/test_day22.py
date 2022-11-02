import pytest

from .day22 import Range, RangeError, Shape


def test_range():
    r = Range(69, 420)
    assert r[0] == r.start == 69
    assert r[1] == r.stop == 420

    r = Range(0, 0)
    assert r[0] == r.start == 0
    assert r[0] == r.stop == 0

    with pytest.raises(RangeError):
        Range(420, 69)


@pytest.mark.parametrize(
    "range, number, inrange",
    [
        (Range(0, 10), -1, False),
        (Range(0, 10), 0, True),
        (Range(0, 10), 5, True),
        (Range(0, 10), 10, False),
        (Range(0, 10), 11, False),
        (Range(0, 0), 0, False),
        (Range(0, 1), 0, True),
        (Range(0, 1), 1, False),
    ],
)
def test_range__contains__(range, number, inrange):
    assert (number in range) == inrange


@pytest.mark.parametrize(
    "range1, range2, expected_ovelaps",
    [
        (Range(0, 2), Range(1, 3), [1, 2]),
        (Range(1, 3), Range(0, 2), [1, 2]),
        (Range(0, 1), Range(1, 2), []),
        (Range(2, 3), Range(1, 4), [2, 3]),
        (Range(0, 4), Range(0, 4), []),
    ],
)
def test_range_get_overlaps(range1, range2, expected_ovelaps):
    assert range1.get_overlaps(range2) == range2.get_overlaps(range1) == expected_ovelaps


@pytest.mark.parametrize(
    "initial_range, breakpoints, expected_output",
    [
        (Range(0, 10), [5], [Range(0, 5), Range(5, 10)]),
        (Range(0, 10), [9], [Range(0, 9), Range(9, 10)]),
        (Range(0, 10), [0], [Range(0, 10)]),
        (Range(0, 10), [10], [Range(0, 10)]),
        (Range(0, 10), [0, 10], [Range(0, 10)]),
    ],
)
def test_range_split(initial_range, breakpoints, expected_output):
    assert initial_range.split(*breakpoints) == expected_output


def test_range_split_error():
    with pytest.raises(RangeError):
        Range(0, 1).split(69)


def test_range_set():
    assert {(0, 2), (0, 2), (0, 2)} == {(0, 2)}
    assert {Range(0, 2), Range(0, 2), Range(0, 2)} == {Range(0, 2)}


def test_shape_set():
    assert {
        Shape(Range(0, 2), Range(0, 2)),
        Shape(Range(0, 2), Range(0, 2)),
        Shape(Range(0, 2), Range(0, 2)),
    } == {Shape(Range(0, 2), Range(0, 2))}


def test_shape_split():
    shape = Shape(Range(0, 10), Range(0, 10))
    assert shape.split([2]) == {
        Shape(Range(0, 2), Range(0, 10)),
        Shape(Range(2, 10), Range(0, 10)),
    }

    assert shape.split([2, 3]) == {
        Shape(Range(0, 2), Range(0, 10)),
        Shape(Range(2, 3), Range(0, 10)),
        Shape(Range(3, 10), Range(0, 10)),
    }

    assert shape.split([2], [3]) == {
        Shape(Range(0, 2), Range(0, 3)),
        Shape(Range(0, 2), Range(3, 10)),
        Shape(Range(2, 10), Range(0, 3)),
        Shape(Range(2, 10), Range(3, 10)),
    }


@pytest.mark.parametrize(
    "x_range, y_range, z_range, expected_count",
    [
        ([0, 1], [0, 1], [], 1),
        ([0, 1], [0, 1], [0, 1], 1),
        ([0, 69], [0, 1], [], 69),
        ([0, 4], [0, 4], [], 16),
        ([0, 3], [0, 3], [], 9),
        ([0, 3], [0, 3], [0, 3], 27),
    ],
)
def test_shape_count(x_range, y_range, z_range, expected_count):
    ranges = [Range(*r) for r in (x_range, y_range, z_range) if r]
    shape = Shape(*ranges)
    assert shape.count() == expected_count


def test_shape_union():
    s1 = Shape(Range(0, 3), Range(0, 3))
    s2 = Shape(Range(2, 5), Range(2, 5))
    expected_result = {
        Shape(Range(0, 2), Range(0, 2)),
        Shape(Range(2, 3), Range(0, 2)),
        Shape(Range(0, 2), Range(2, 3)),
        Shape(Range(2, 3), Range(2, 3)),
        Shape(Range(2, 3), Range(3, 5)),
        Shape(Range(3, 5), Range(2, 3)),
        Shape(Range(3, 5), Range(3, 5)),
    }
    assert s1.union(s2) == s2.union(s1) == expected_result


def test_shape_difference():
    s1 = Shape(Range(0, 3), Range(0, 3))
    s2 = Shape(Range(2, 5), Range(2, 5))
    assert s1.difference(s2) == {
        Shape(Range(0, 2), Range(0, 2)),
        Shape(Range(2, 3), Range(0, 2)),
        Shape(Range(0, 2), Range(2, 3)),
    }
    assert s2.difference(s1) == {
        Shape(Range(2, 3), Range(3, 5)),
        Shape(Range(3, 5), Range(2, 3)),
        Shape(Range(3, 5), Range(3, 5)),
    }
