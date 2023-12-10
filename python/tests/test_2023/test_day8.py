import pytest

from puzzles.y2023.day8 import *

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

example3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def test_part1():
    assert part1(example1) == 2
    assert part1(example2) == 6


def test__parse_input():
    assert parse_input(example2) == (
        "LLR",
        {
            "AAA": ("BBB", "BBB"),
            "BBB": ("AAA", "ZZZ"),
            "ZZZ": ("ZZZ", "ZZZ"),
        },
    )


def test_part2():
    assert part2(example3) == 6


def test_simulate_endpoints():
    """
    If our function to calculate the endpoints is correct, it should match the brute force one
    that simulates every step.
    """
    instructions, nodes = parse_input(example2)
    simulated = simulate_endpoints("AAA", 10, instructions, nodes)
    assert len(simulated) == 10
    calculated = calculate_endpoints("AAA", 10, instructions, nodes)
    assert len(calculated) == 10
    simulated2 = simulate_endpoints2("AAA", 10, instructions, nodes)
    assert len(simulated2) == 10
    assert simulated == calculated
    assert simulated == simulated2


def test_simulate_trajectory():
    instructions, nodes = parse_input(example2)
    steps = simulate_trajectory("AAA", instructions, nodes)
    assert steps == [
        (0, "AAA"),
        (1, "BBB"),
        (2, "AAA"),
        (3, "BBB"),
        (4, "AAA"),
        (5, "BBB"),
        (6, "ZZZ"),
    ]


@pytest.mark.parametrize(
    "start_node, input, expected_intro, expected_loop",
    [
        (
            "11A",
            example3,
            [(0, "11A")],
            [
                (1, "11B"),
                (0, "11Z"),
            ],
        ),
        (
            "22A",
            example3,
            [(0, "22A")],
            [
                (1, "22B"),
                (0, "22C"),
                (1, "22Z"),
                (0, "22B"),
                (1, "22C"),
                (0, "22Z"),
            ],
        ),
    ],
)
def test_find_cycle(
    start_node,
    input,
    expected_intro,
    expected_loop,
):
    instructions, nodes = parse_input(input)
    intro, loop = find_cycle(start_node, instructions, nodes)
    assert intro == expected_intro
    assert loop == expected_loop
