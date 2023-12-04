import utils
import re

Numbers = list[int]


@utils.profile
def part1(input: str):
    cards = _parse_input(input)
    result = 0
    for card_num, winning_numbers, your_numbers in cards:
        result += _score_card(winning_numbers, your_numbers)
    return result


@utils.profile
def part2(input: str):
    cards = _parse_input(input)
    duplicates = {card_num: 1 for card_num, _, _ in cards}
    for card_num, winning_numbers, your_numbers in cards:
        score = _num_matches(winning_numbers, your_numbers)
        num_copies = duplicates[card_num]
        for ii in range(1, score + 1):  # duplicate the next N cards
            index = card_num + ii
            duplicates[index] += num_copies
    return sum(duplicates.values())


def _num_matches(winning_numbers: Numbers, your_numbers: Numbers) -> int:
    matches = 0
    for n in your_numbers:
        if n in winning_numbers:
            matches += 1
    return matches


def _score_card(winning_numbers: Numbers, your_numbers: Numbers) -> int:
    matches = _num_matches(winning_numbers, your_numbers)
    if not matches:
        return matches
    return 2 ** (matches - 1)


def _parse_input(input: str) -> list[tuple[int, Numbers, Numbers]]:
    lines = list(map(str.strip, input.splitlines()))
    return [_parse_line(line) for line in lines]


def _parse_line(line: str) -> tuple[int, Numbers, Numbers]:
    rx = re.compile(r"Card +(\d+): (.*) \| (.*)")
    match = rx.match(line)
    if not match:
        raise Exception(f"couldn't find match for {line}")
    card_no, winning_nos, your_nos = match.groups()
    card_no = int(card_no)
    winning_nos = list(map(int, re.findall(r"(\d+)", winning_nos)))
    your_nos = list(map(int, re.findall(r"(\d+)", your_nos)))
    return card_no, winning_nos, your_nos


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day4")
    assert part1(input) == 18653
    assert part2(input) == 5921508
