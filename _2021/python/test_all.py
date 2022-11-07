import pytest

from _2021.python import (
    day1,
    day2,
    day3,
    day4,
    day5,
    day6,
    day7,
    day8,
    day9,
    day10,
    day11,
    day12,
    day13,
    day14,
    day15,
    day16,
    day17,
    day18,
    day19,
    day20,
    day21,
    day25,
    day22,
)


@pytest.mark.parametrize(
    "module, func, expected_output",
    [
        (day1, "part1", 1482),
        (day1, "part2", 1518),
        (day2, "part1", 1451208),
        (day2, "part2", 1620141160),
        (day3, "part1", 3549854),
        (day3, "part2", 3765399),
        (day4, "part1", 33348),
        (day4, "part2", 8112),
        (day5, "part1", 7644),
        (day5, "part2", 18627),
        (day6, "part1", 374927),
        (day6, "part2", 1687617803407),
        (day7, "part1", 333755),
        (day7, "part2", 94017638),
        (day8, "part1", 303),
        (day8, "part2", 961734),
        (day9, "part1", 4),
        (day9, "part2", 144),
        (day10, "part1", 168417),
        (day10, "part2", 2802519786),
        (day11, "part1", 1721),
        (day11, "part2", 298),
        (day12, "part1", 4912),
        (day12, "part2", 150004),
        (day13, "part1", 655),
        (day13, "part2", 95),
        (day14, "part1", 2590),
        (day14, "part2", 2875665202438),
        (day15, "part1", 423),
        (day15, "part2", 2778),
        (day16, "part1", 934),
        (day16, "part2", 912901337844),
        (day17, "part1", 5565),
        (day17, "part2", 2118),
        (day18, "part1", 4243),
        (day18, "part2", 4701),
        (day19, "part1", 428),
        (day19, "part2", 12140),
        (day20, "part1", 5225),
        (day20, "part2", 18131),
        (day21, "part1", 1073709),
        # (day21, "part2", None),
        (day22, "part1", 533863),
        (day22, "part2", 1261885414840992),
        # (day23, "part1", None),
        # (day23, "part2", None),
        # (day24, "part1", None),
        # (day24, "part2", None),
        (day25, "part1", 295),
        # (day25, "part2", None),
    ],
)
def test(module, func, expected_output):
    func = getattr(module, func)
    assert func() == expected_output
