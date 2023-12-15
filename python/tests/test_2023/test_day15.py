import pytest

from puzzles.y2023.day15 import *

example = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def test_part1():
    assert part1(example) == 1320


def test_part2():
    assert part2(example) == 145


def test_build_hashmap():
    steps = parse_input(example)
    hashmap = build_hashmap(steps)
    for box in range(256):
        if box == 0:
            assert hashmap[box] == [("rn", 1), ("cm", 2)]
        elif box == 3:
            assert hashmap[box] == [("ot", 7), ("ab", 5), ("pc", 6)]
        else:
            assert hashmap[box] == []


@pytest.mark.parametrize(
    "step, expected",
    [
        ("rn=1", (hash("rn"), "rn", "=", "1")),
        ("cm-", (hash("cm"), "cm", "-", "")),
        ("qp=3", (hash("qp"), "qp", "=", "3")),
        ("cm=2", (hash("cm"), "cm", "=", "2")),
    ],
)
def test_parse_step(step, expected):
    assert parse_step(step) == expected


def test_hash():
    assert hash("HASH") == 52
