from puzzles.y2023 import day8

example1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def test_part1():
    assert day8.part1(example1) == 2
    assert day8.part1(example2) == 6


def test__parse_input():
    assert day8._parse_input(example2) == (
        "LLR",
        [
            ("AAA", "BBB", "BBB"),
            ("BBB", "AAA", "ZZZ"),
            ("ZZZ", "ZZZ", "ZZZ"),
        ],
    )
