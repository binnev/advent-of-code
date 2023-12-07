from enum import Enum

import utils


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


STRENGTH = "23456789TJQKA"


@utils.profile
def part1(input: str) -> int:
    hands = _parse_input(input)
    rank = _rank_hands(list(hands))
    result = 0
    for hand, bid in hands.items():
        value = rank[hand] * bid
        result += value
    return result


@utils.profile
def part2(input: str):
    ...


def _compare_hands(left: str, right: str) -> str:
    left_type = _hand_type(left)
    right_type = _hand_type(right)

    # one hand outright beats the other because it's a better type
    if left_type.value > right_type.value:
        return left
    if right_type.value > left_type.value:
        return right

    # the hands are the same type so we compare cards
    for l, r in zip(left, right):
        l_strength = STRENGTH.index(l)
        r_strength = STRENGTH.index(r)
        if l_strength == r_strength:
            continue
        elif l_strength > r_strength:
            return left
        else:
            return right

    return None  # draw


def _hand_type(hand: str) -> HandType:
    unique = set(hand)
    counts = sorted(hand.count(card) for card in unique)

    if len(unique) == 1:
        return HandType.FIVE_OF_A_KIND
    elif len(unique) == 2:
        if counts == [1, 4]:
            return HandType.FOUR_OF_A_KIND
        if counts == [2, 3]:
            return HandType.FULL_HOUSE
    elif len(unique) == 3:
        if counts == [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        if counts == [1, 2, 2]:
            return HandType.TWO_PAIR
    elif len(unique) == 4:
        if counts == [1, 1, 1, 2]:
            return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def _parse_input(input: str) -> dict[str, int]:
    output = {}
    for line in input.splitlines():
        hand, bid = line.split()
        output[hand] = int(bid)
    return output


def _absolute_strength(hand: str) -> int:
    """
    hand_type -> 10_000_000_000
    1st card -> 100_000_000
    2nd card -> 1_000_000
    3rd card -> 10_000
    4th card -> 100
    5th card -> 1
    """
    strength = _hand_type(hand).value * 10_000_000_000
    card_weights = [
        100_000_000,  # 1st card
        1_000_000,  # 2nd card
        10_000,  # 3rd card
        100,  # 4th card
        1,  # 5th card
    ]
    for card, weight in zip(hand, card_weights):
        strength += STRENGTH.index(card) * weight
    return strength


def _rank_hands(hands: list[str]) -> dict[str, int]:
    absolute_strengths = {hand: _absolute_strength(hand) for hand in hands}
    ranked = sorted(hands, key=lambda hand: absolute_strengths[hand])
    return {hand: ranked.index(hand) + 1 for hand in hands}


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day7")
    part1(input)
    part2(input)
