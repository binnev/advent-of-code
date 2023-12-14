import pytest

from puzzles import y2020, y2021, y2022, y2023
from utils import load_puzzle_input

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(
    "day, func, expected_output",
    [
        ("2020/day1", y2020.day1.part1, 145875),
        ("2020/day1", y2020.day1.part2, 69596112),
        ("2020/day2", y2020.day2.part1, 628),
        ("2020/day2", y2020.day2.part2, 705),
    ],
)
def test_2020(day, func, expected_output):
    raw = load_puzzle_input(day)
    assert func(raw) == expected_output


@pytest.mark.parametrize(
    "day, func, expected_output",
    [
        ("2021/day1", y2021.day1.part1, 1482),
        ("2021/day1", y2021.day1.part2, 1518),
        ("2021/day2", y2021.day2.part1, 1451208),
        ("2021/day2", y2021.day2.part2, 1620141160),
        ("2021/day3", y2021.day3.part1, 3549854),
        ("2021/day3", y2021.day3.part2, 3765399),
        ("2021/day4", y2021.day4.part1, 33348),
        ("2021/day4", y2021.day4.part2, 8112),
        ("2021/day5", y2021.day5.part1, 7644),
        ("2021/day5", y2021.day5.part2, 18627),
        ("2021/day6", y2021.day6.part1, 374927),
        ("2021/day6", y2021.day6.part2, 1687617803407),
        ("2021/day7", y2021.day7.part1, 333755),
        ("2021/day7", y2021.day7.part2, 94017638),
        ("2021/day8", y2021.day8.part1, 303),
        ("2021/day8", y2021.day8.part2, 961734),
        ("2021/day9", y2021.day9.part1, 4),
        ("2021/day9", y2021.day9.part2, 144),
        ("2021/day10", y2021.day10.part1, 168417),
        ("2021/day10", y2021.day10.part2, 2802519786),
        ("2021/day11", y2021.day11.part1, 1721),
        ("2021/day11", y2021.day11.part2, 298),
        ("2021/day12", y2021.day12.part1, 4912),
        ("2021/day12", y2021.day12.part2, 150004),
        ("2021/day13", y2021.day13.part1, 655),
        ("2021/day13", y2021.day13.part2, 95),
        ("2021/day14", y2021.day14.part1, 2590),
        ("2021/day14", y2021.day14.part2, 2875665202438),
        ("2021/day15", y2021.day15.part1, 423),
        ("2021/day15", y2021.day15.part2, 2778),
        ("2021/day16", y2021.day16.part1, 934),
        ("2021/day16", y2021.day16.part2, 912901337844),
        ("2021/day17", y2021.day17.part1, 5565),
        ("2021/day17", y2021.day17.part2, 2118),
        ("2021/day18", y2021.day18.part1, 4243),
        ("2021/day18", y2021.day18.part2, 4701),
        ("2021/day19", y2021.day19.part1, 428),
        ("2021/day19", y2021.day19.part2, 12140),
        ("2021/day20", y2021.day20.part1, 5225),
        ("2021/day20", y2021.day20.part2, 18131),
        ("2021/day21", y2021.day21.part1, 1073709),
        # ("2021/day21", y2021.day21.part2, None),
        ("2021/day22", y2021.day22.part1, 533863),
        ("2021/day22", y2021.day22.part2, 1261885414840992),
        # ("2021/day23", y2021.day23.part1, None),
        # ("2021/day23", y2021.day23.part2, None),
        # ("2021/day24", y2021.day24.part1, None),
        # ("2021/day24", y2021.day24.part2, None),
        ("2021/day25", y2021.day25.part1, 295),
        # ("2021/day25", y2021.day25.part2, None),
    ],
)
def test_2021(day, func, expected_output):
    raw = load_puzzle_input(day)
    assert func(raw) == expected_output


@pytest.mark.parametrize(
    "day, func, expected_output",
    [
        ("2022/day1", y2022.day1.part1, 66186),
        ("2022/day1", y2022.day1.part2, 196804),
        ("2022/day2", y2022.day2.part1, 14264),
        ("2022/day2", y2022.day2.part2, 12382),
        ("2022/day3", y2022.day3.part1, 8233),
        ("2022/day3", y2022.day3.part2, 2821),
        ("2022/day4", y2022.day4.part1, 567),
        ("2022/day4", y2022.day4.part2, 907),
        ("2022/day5", y2022.day5.part1, "GRTSWNJHH"),
        ("2022/day5", y2022.day5.part2, "QLFQDBBHM"),
        ("2022/day6", y2022.day6.part1, 1175),
        ("2022/day6", y2022.day6.part2, 3217),
        ("2022/day7", y2022.day7.part1, 1792222),
        ("2022/day7", y2022.day7.part2, 1112963),
        ("2022/day8", y2022.day8.part1, 1698),
        ("2022/day8", y2022.day8.part2, 672280),
        ("2022/day9", y2022.day9.part1, 6494),
        ("2022/day9", y2022.day9.part2, 2691),
        ("2022/day10", y2022.day10.part1, 13440),
        (
            "2022/day10",
            y2022.day10.part2,
            (
                "###  ###  ####  ##  ###   ##  ####  ##  \n"
                "#  # #  #    # #  # #  # #  #    # #  # \n"
                "#  # ###    #  #    #  # #  #   #  #  # \n"
                "###  #  #  #   # ## ###  ####  #   #### \n"
                "#    #  # #    #  # # #  #  # #    #  # \n"
                "#    ###  ####  ### #  # #  # #### #  # "
            ),
        ),
        ("2022/day11", y2022.day11.part1, 64032),
        ("2022/day11", y2022.day11.part2, 12729522272),
        ("2022/day12", y2022.day12.part1, 440),
        ("2022/day12", y2022.day12.part2, 439),
        ("2022/day13", y2022.day13.part1, 6420),
        ("2022/day13", y2022.day13.part2, 22000),
        ("2022/day14", y2022.day14.part1, 755),
        ("2022/day14", y2022.day14.part2, 29805),
        ("2022/day15", y2022.day15.part1, 5716881),
        ("2022/day15", y2022.day15.part2, 10852583132904),
        ("2022/day16", y2022.day16.part1, 2056),
        ("2022/day16", y2022.day16.part2, 2513),
        ("2022/day17", y2022.day17.part1, 3109),
        ("2022/day17", y2022.day17.part2, 1541449275365),
        ("2022/day18", y2022.day18.part1, 4628),
        ("2022/day18", y2022.day18.part2, 2582),
        ("2022/day19", y2022.day19.part1, 1766),
        ("2022/day19", y2022.day19.part2, 30780),
        ("2022/day20", y2022.day20.part1, 14888),
        ("2022/day20", y2022.day20.part2, 3760092545849),
        ("2022/day21", y2022.day21.part1, 142707821472432),
        ("2022/day21", y2022.day21.part2, 3587647562851),
        ("2022/day22", y2022.day22.part1, 65368),
        ("2022/day22", y2022.day22.part2, 156166),
        ("2022/day23", y2022.day23.part1, 4236),
        ("2022/day23", y2022.day23.part2, 1023),
        ("2022/day24", y2022.day24.part1, 228),
        ("2022/day24", y2022.day24.part2, 723),
        ("2022/day25", y2022.day25.part1, "20-1-0=-2=-2220=0011"),
    ],
)
def test_2022(day, func, expected_output):
    raw = load_puzzle_input(day)
    assert func(raw) == expected_output


@pytest.mark.parametrize(
    "day, func, expected_output",
    [
        ("2023/day1", y2023.day1.part1, 55123),
        ("2023/day1", y2023.day1.part2, 55260),
        ("2023/day2", y2023.day2.part1, 1853),
        ("2023/day2", y2023.day2.part2, 72706),
        ("2023/day3", y2023.day3.part1, 527369),
        ("2023/day3", y2023.day3.part2, 73074886),
        ("2023/day4", y2023.day4.part1, 18653),
        ("2023/day4", y2023.day4.part2, 5921508),
        ("2023/day5", y2023.day5.part1, 174137457),
        ("2023/day5", y2023.day5.part2, 1493866),
        ("2023/day6", y2023.day6.part1, 1413720),
        ("2023/day6", y2023.day6.part2, 30565288),
        ("2023/day7", y2023.day7.part1, 248422077),
        ("2023/day7", y2023.day7.part2, 249817836),
        ("2023/day8", y2023.day8.part1, 14681),
        # ("2023/day8", y2023.day8.part2, ???),
        ("2023/day9", y2023.day9.part1, 1887980197),
        ("2023/day9", y2023.day9.part2, 990),
        ("2023/day11", y2023.day11.part1, 9536038),
        ("2023/day11", y2023.day11.part2, 447744640566),
        ("2023/day14", y2023.day14.part1, 112048),
        ("2023/day14", y2023.day14.part2, 105606),
    ],
)
def test_2023(day, func, expected_output):
    raw = load_puzzle_input(day)
    assert func(raw) == expected_output
