import pytest

from puzzles.y2023 import day5

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


def test__parse_input():
    seeds, transforms = day5._parse_input(example1)
    assert seeds == [79, 14, 55, 13]
    assert isinstance(transforms[0], dict)
    assert len(transforms) == 7
    assert transforms[0] == {
        range(98, 100): range(50, 52),
        range(50, 50 + 48): range(52, 52 + 48),
    }


def test__parse_ranges():
    src_range, dst_range = day5._parse_range_line("50 98 2")
    assert src_range == range(98, 100)
    assert dst_range == range(50, 52)

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
