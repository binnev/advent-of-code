import pytest

from python import _2020, _2021, _2022


@pytest.mark.parametrize(
    "func, expected_output",
    [
        (_2020.day1.part1, 145875),
        (_2020.day1.part2, 69596112),
        (_2020.day2.part1, 628),
        (_2020.day2.part2, 705),
    ],
)
def test_2020(func, expected_output):
    assert func() == expected_output


@pytest.mark.parametrize(
    "func, expected_output",
    [
        (_2021.day1.part1, 1482),
        (_2021.day1.part2, 1518),
        (_2021.day2.part1, 1451208),
        (_2021.day2.part2, 1620141160),
        (_2021.day3.part1, 3549854),
        (_2021.day3.part2, 3765399),
        (_2021.day4.part1, 33348),
        (_2021.day4.part2, 8112),
        (_2021.day5.part1, 7644),
        (_2021.day5.part2, 18627),
        (_2021.day6.part1, 374927),
        (_2021.day6.part2, 1687617803407),
        (_2021.day7.part1, 333755),
        (_2021.day7.part2, 94017638),
        (_2021.day8.part1, 303),
        (_2021.day8.part2, 961734),
        (_2021.day9.part1, 4),
        (_2021.day9.part2, 144),
        (_2021.day10.part1, 168417),
        (_2021.day10.part2, 2802519786),
        (_2021.day11.part1, 1721),
        (_2021.day11.part2, 298),
        (_2021.day12.part1, 4912),
        (_2021.day12.part2, 150004),
        (_2021.day13.part1, 655),
        (_2021.day13.part2, 95),
        (_2021.day14.part1, 2590),
        (_2021.day14.part2, 2875665202438),
        (_2021.day15.part1, 423),
        (_2021.day15.part2, 2778),
        (_2021.day16.part1, 934),
        (_2021.day16.part2, 912901337844),
        (_2021.day17.part1, 5565),
        (_2021.day17.part2, 2118),
        (_2021.day18.part1, 4243),
        (_2021.day18.part2, 4701),
        (_2021.day19.part1, 428),
        (_2021.day19.part2, 12140),
        (_2021.day20.part1, 5225),
        (_2021.day20.part2, 18131),
        (_2021.day21.part1, 1073709),
        # (_2021.day21.part2, None),
        (_2021.day22.part1, 533863),
        (_2021.day22.part2, 1261885414840992),
        # (_2021.day23.part1, None),
        # (_2021.day23.part2, None),
        # (_2021.day24.part1, None),
        # (_2021.day24.part2, None),
        (_2021.day25.part1, 295),
        # (_2021.day25.part2, None),
    ],
)
def test_2021(func, expected_output):
    assert func() == expected_output


@pytest.mark.parametrize(
    "func, expected_output",
    [
        (_2022.day1.part1, 66186),
        (_2022.day1.part2, 196804),
        (_2022.day2.part1, 14264),
        (_2022.day2.part2, 12382),
        (_2022.day3.part1, 8233),
        (_2022.day3.part2, 2821),
        (_2022.day4.part1, 567),
        (_2022.day4.part2, 907),
        (_2022.day5.part1, "GRTSWNJHH"),
        (_2022.day5.part2, "QLFQDBBHM"),
    ],
)
def test_2022(func, expected_output):
    assert func() == expected_output
