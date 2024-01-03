from enum import Enum
from functools import cmp_to_key

import utils


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


@utils.profile
def part1(input: str) -> int:
    hands = _parse_input(input)
    rank = _rank_hands(list(hands))
    result = sum(rank[hand] * bid for hand, bid in hands.items())
    return result


@utils.profile
def part2(input: str):
    hands = _parse_input(input)
    rank = _rank_hands(list(hands), jokers=True)
    result = sum(rank[hand] * bid for hand, bid in hands.items())
    return result


def _card_strength(card: str, jokers=False) -> int:
    if jokers:
        return "J23456789TJQKA".index(card)
    else:
        return "23456789TJQKA".index(card)


def _hand_type(hand: str, jokers=False) -> HandType:
    if jokers and "J" in hand:
        joker_card = _best_joker_value(hand)
        hand = hand.replace("J", joker_card)

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


def _compare_hands(left: str, right: str, jokers=False) -> str | None:
    left_type = _hand_type(left, jokers)
    right_type = _hand_type(right, jokers)

    # one hand outright beats the other because it's a better type
    if left_type.value > right_type.value:
        return left
    if right_type.value > left_type.value:
        return right

    # the hands are the same type so we compare cards
    for l, r in zip(left, right):
        l_strength = _card_strength(l, jokers)
        r_strength = _card_strength(r, jokers)
        if l_strength == r_strength:
            continue
        elif l_strength > r_strength:
            return left
        else:
            return right

    return None  # draw


def _best_joker_value(hand: str) -> str:
    """
    Choose the joker value that will maximise the value of the hand
    """
    other_cards = hand.replace("J", "")

    if not other_cards:  # because the hand is all jokers
        return "A"

    best_card = other_cards[0]
    best_count = hand.count(best_card)
    for card in other_cards:
        count = hand.count(card)
        # better hand types should always be prioritised
        if count > best_count:
            best_card = card
            best_count = count
        # if hand types would be the same, choose the stronger card
        elif count == best_count:
            if _card_strength(card, jokers=True) > _card_strength(best_card, jokers=True):
                best_card = card
                best_count = count

    return best_card


def _parse_input(input: str) -> dict[str, int]:
    output = {}
    for line in input.splitlines():
        hand, bid = line.split()
        output[hand] = int(bid)
    return output


def _rank_hands(hands: list[str], jokers=False) -> dict[str, int]:
    """
    We need to sort using a comparison function because we have no absolute value for hand
    strength.
    """

    def cmp(left, right):
        winner = _compare_hands(left, right, jokers)
        if winner == left:
            return 1
        elif winner == right:
            return -1
        else:
            return 0

    ranked = sorted(hands, key=cmp_to_key(cmp))
    return {hand: ranked.index(hand) + 1 for hand in hands}
