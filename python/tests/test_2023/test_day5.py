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
        Transform({Range(2, 9): Range(1, 8)}),
        Transform({Range(5, 10): Range(6, 11)}),
        Transform({Range(7, 9): Range(3, 5)}),
        Transform({Range(2, 6): Range(3, 7)}),
    ]
    critical_points = day5._find_critical_points(transforms)
    expected = {2, 3, 6, 7, 9, 10}
    assert critical_points == expected


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
def test_transform_forwards(input, expected):
    transform = Transform()
    for line in "50 98 2", "52 50 48":
        src, dst = day5._parse_range_line(line)
        transform[src] = dst

    out = transform.forwards(input)
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
def test__apply_transforms(input, expected):
    _, transforms = day5._parse_input(example1)
    result = day5._apply_transforms(input, transforms)
    assert result == expected


def test_part1():
    assert day5.part1(example1) == 35


def test_part2():
    assert day5.part2(example1) == 46

    """
    It's too slow because we're trying to simulate it all. 
    What we instead need to do is create a function that _merges RangeMaps_. 
    
    """
