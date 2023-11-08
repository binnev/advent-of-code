import pytest

from puzzles import y2020, y2021, y2022
from utils import load_puzzle_input


@pytest.mark.parametrize(
    "func, input, expected_output",
    [
        (y2020.day1.part1, load_puzzle_input("2020/day1"), 145875),
        (y2020.day1.part2, load_puzzle_input("2020/day1"), 69596112),
        (y2020.day2.part1, load_puzzle_input("2020/day2"), 628),
        (y2020.day2.part2, load_puzzle_input("2020/day2"), 705),
    ],
)
def test_2020(func, input, expected_output):
    assert func(input) == expected_output


@pytest.mark.parametrize(
    "func, expected_output",
    [
        (y2021.day1.part1, 1482),
        (y2021.day1.part2, 1518),
        (y2021.day2.part1, 1451208),
        (y2021.day2.part2, 1620141160),
        (y2021.day3.part1, 3549854),
        (y2021.day3.part2, 3765399),
        (y2021.day4.part1, 33348),
        (y2021.day4.part2, 8112),
        (y2021.day5.part1, 7644),
        (y2021.day5.part2, 18627),
        (y2021.day6.part1, 374927),
        (y2021.day6.part2, 1687617803407),
        (y2021.day7.part1, 333755),
        (y2021.day7.part2, 94017638),
        (y2021.day8.part1, 303),
        (y2021.day8.part2, 961734),
        (y2021.day9.part1, 4),
        (y2021.day9.part2, 144),
        (y2021.day10.part1, 168417),
        (y2021.day10.part2, 2802519786),
        (y2021.day11.part1, 1721),
        (y2021.day11.part2, 298),
        (y2021.day12.part1, 4912),
        (y2021.day12.part2, 150004),
        (y2021.day13.part1, 655),
        (y2021.day13.part2, 95),
        (y2021.day14.part1, 2590),
        (y2021.day14.part2, 2875665202438),
        (y2021.day15.part1, 423),
        (y2021.day15.part2, 2778),
        (y2021.day16.part1, 934),
        (y2021.day16.part2, 912901337844),
        (y2021.day17.part1, 5565),
        (y2021.day17.part2, 2118),
        (y2021.day18.part1, 4243),
        (y2021.day18.part2, 4701),
        (y2021.day19.part1, 428),
        (y2021.day19.part2, 12140),
        (y2021.day20.part1, 5225),
        (y2021.day20.part2, 18131),
        (y2021.day21.part1, 1073709),
        # (_2021.day21.part2, None),
        (y2021.day22.part1, 533863),
        (y2021.day22.part2, 1261885414840992),
        # (_2021.day23.part1, None),
        # (_2021.day23.part2, None),
        # (_2021.day24.part1, None),
        # (_2021.day24.part2, None),
        (y2021.day25.part1, 295),
        # (_2021.day25.part2, None),
    ],
)
def test_2021(func, expected_output):
    assert func() == expected_output


@pytest.mark.parametrize(
    "func, expected_output",
    [
        (y2022.day1.part1, 66186),
        (y2022.day1.part2, 196804),
        (y2022.day2.part1, 14264),
        (y2022.day2.part2, 12382),
        (y2022.day3.part1, 8233),
        (y2022.day3.part2, 2821),
        (y2022.day4.part1, 567),
        (y2022.day4.part2, 907),
        (y2022.day5.part1, "GRTSWNJHH"),
        (y2022.day5.part2, "QLFQDBBHM"),
        (y2022.day6.part1, 1175),
        (y2022.day6.part2, 3217),
        (y2022.day7.part1, 1792222),
        (y2022.day7.part2, 1112963),
        (y2022.day8.part1, 1698),
        (y2022.day8.part2, 672280),
        (y2022.day9.part1, 6494),
        (y2022.day9.part2, 2691),
        (y2022.day10.part1, 13440),
        (
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
        (y2022.day11.part1, 64032),
        (y2022.day11.part2, 12729522272),
        (y2022.day12.part1, 440),
        (y2022.day12.part2, 439),
        (y2022.day13.part1, 6420),
        (y2022.day13.part2, 22000),
        (y2022.day14.part1, 755),
        (y2022.day14.part2, 29805),
        (y2022.day15.part1, 5716881),
        # (_2022.day15.part2, 10852583132904), # way too slow
        # (_2022.day16.part1, 2056),  # way too slow
        # (_2022.day16.part2, 2513),  # way too slow
        (y2022.day17.part1, 3109),
        (y2022.day17.part2, 1541449275365),
        (y2022.day18.part1, 4628),
        (y2022.day18.part2, 2582),
        # (_2022.day19.part1, 1766),  # way too slow
        # (_2022.day19.part2, 30780),  # way too slow
        (y2022.day20.part1, 14888),
        (y2022.day20.part2, 3760092545849),
        (y2022.day21.part1, 142707821472432),
        (y2022.day21.part2, 3587647562851),
        (y2022.day22.part1, 65368),
        (y2022.day22.part2, 156166),
        (y2022.day23.part1, 4236),
        (y2022.day23.part2, 1023),
        (y2022.day24.part1, 228),
        # (_2022.day24.part2, 723),  # takes 16 seconds
        (y2022.day25.part1, "20-1-0=-2=-2220=0011"),
    ],
)
def test_2022(func, expected_output):
    assert func() == expected_output
