import pytest

from puzzles.y2023 import day7
from puzzles.y2023.day7 import HandType

example1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test__parse_input():
    assert day7._parse_input(example1) == {
        "32T3K": 765,
        "T55J5": 684,
        "KK677": 28,
        "KTJJT": 220,
        "QQQJA": 483,
    }


def test_part1():
    assert day7.part1(example1) == 6440


def test_part2():
    assert day7.part2(example1) == 5905


@pytest.mark.parametrize(
    "hand, expected_type",
    [
        ("AAAAA", HandType.FIVE_OF_A_KIND),
        ("AA8AA", HandType.FOUR_OF_A_KIND),
        ("23332", HandType.FULL_HOUSE),
        ("TTT98", HandType.THREE_OF_A_KIND),
        ("23432", HandType.TWO_PAIR),
        ("A23A4", HandType.ONE_PAIR),
        ("23456", HandType.HIGH_CARD),
    ],
)
def test__hand_type(hand, expected_type):
    assert day7._hand_type(hand) == expected_type


@pytest.mark.parametrize(
    "hand, expected_type",
    [
        ("32T3K", HandType.ONE_PAIR),
        ("T55J5", HandType.FOUR_OF_A_KIND),
        ("KK677", HandType.TWO_PAIR),
        ("KTJJT", HandType.FOUR_OF_A_KIND),
        ("QQQJA", HandType.FOUR_OF_A_KIND),
    ],
)
def test__hand_type_with_jokers(hand, expected_type):
    assert day7._hand_type(hand, jokers=True) == expected_type


@pytest.mark.parametrize(
    "left, right, expected_winner",
    [
        ("33332", "2AAAA", "33332"),
        ("77888", "77788", "77888"),
        ("AAAAA", "AAAAA", None),
    ],
)
def test__compare_hands(left, right, expected_winner):
    assert day7._compare_hands(left, right) == expected_winner


@pytest.mark.parametrize(
    "left, right, expected_winner",
    [
        ("T55J5", "QQQJA", "QQQJA"),
        ("T55J5", "KTJJT", "KTJJT"),
        ("QQQJA", "KTJJT", "KTJJT"),
    ],
)
def test__compare_hands_with_jokers(left, right, expected_winner):
    assert day7._compare_hands(left, right, jokers=True) == expected_winner


def test_compare_hand_type():
    hand1 = HandType.FULL_HOUSE
    hand2 = HandType.TWO_PAIR
    assert hand1.value > hand2.value


def test__rank_hands():
    hands = [
        "32T3K",
        "T55J5",
        "KK677",
        "KTJJT",
        "QQQJA",
    ]
    ranked = day7._rank_hands(hands)
    assert ranked == {
        "32T3K": 1,
        "KTJJT": 2,
        "KK677": 3,
        "T55J5": 4,
        "QQQJA": 5,
    }


def test__rank_hands_with_jokers():
    hands = [
        "32T3K",
        "T55J5",
        "KK677",
        "KTJJT",
        "QQQJA",
    ]
    ranked = day7._rank_hands(hands, jokers=True)
    assert ranked == {
        "32T3K": 1,
        "KK677": 2,
        "T55J5": 3,
        "QQQJA": 4,
        "KTJJT": 5,
    }
