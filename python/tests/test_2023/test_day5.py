import pytest

from puzzles.y2023 import day5
from puzzles.y2023.day5 import Transform, Range

example1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test__find_critical_points():
    transforms = [
        Transform({(2, 9): (1, 8)}),
        Transform({(5, 10): (6, 11)}),
        Transform({(7, 9): (3, 5)}),
        Transform({(2, 6): (3, 7)}),
    ]
    critical_points = day5._find_critical_points(transforms)
    expected = {2, 3, 6, 7, 9, 10}
    assert critical_points == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        pytest.param(
            (10, 12),
            (12, 14),
            [(10, 11), (12, 12), (13, 14)],
            id="single overlap",
        ),
        pytest.param(
            (10, 12),
            (11, 13),
            [(10, 10), (11, 12), (13, 13)],
            id="double overlap",
        ),
        pytest.param(
            (0, 10),
            (4, 6),
            [(0, 3), (4, 6), (7, 10)],
            id="one contains the other ",
        ),
    ],
)
def test__intersect(first, second, expected):
    assert day5._intersect(first, second) == expected


@pytest.mark.parametrize(
    "left, right, should_overlap",
    [
        ((0, 1), (2, 3), False),  # no overlap; just touching
        ((0, 2), (2, 3), True),  # single overlap
        ((0, 2), (1, 3), True),  # multiple overlap
        ((0, 10), (4, 5), True),  # one contains the other
    ],
)
def test__ranges_overlap(left, right, should_overlap):
    assert day5._overlaps(left, right) == should_overlap
    assert day5._overlaps(right, left) == should_overlap


def test__parse_input():
    seeds, transforms = day5._parse_input(example1)
    assert seeds == [79, 14, 55, 13]
    assert isinstance(transforms[0], dict)
    assert len(transforms) == 7
    assert transforms[0] == {
        (98, 99): (50, 51),
        (50, 97): (52, 99),
    }


def test__parse_ranges():
    src_range, dst_range = day5._parse_range_line("50 98 2")
    assert src_range == (98, 99)
    assert dst_range == (50, 51)

    assert 97 not in src_range
    assert 98 in src_range
    assert 99 in src_range
    assert 100 not in src_range

    assert 49 not in dst_range
    assert 50 in dst_range
    assert 51 in dst_range
    assert 52 not in dst_range


@pytest.mark.parametrize(
    "input, expected",
    [
        (0, 0),
        (10, 10),
        (49, 49),
        (50, 52),
        (51, 53),
        (96, 98),
        (97, 99),
        (98, 50),
        (99, 51),
    ],
)
def test__apply_map(input, expected):
    range_map = day5.Transform()
    for line in "50 98 2", "52 50 48":
        src, dst = day5._parse_range_line(line)
        range_map[src] = dst

    out = day5._apply_map(input, range_map)
    assert out == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (79, 82),
        (14, 43),
        (55, 86),
        (13, 35),
    ],
)
def test__calculate_seed(input, expected):
    _, transforms = day5._parse_input(example1)
    result = day5._calculate_seed(input, transforms)
    assert result == expected


def test_part1():
    assert day5.part1(example1) == 35


def test_part2():
    assert day5.part2(example1) == 46

    """
    It's too slow because we're trying to simulate it all. 
    What we instead need to do is create a function that _merges RangeMaps_. 
    
    """
