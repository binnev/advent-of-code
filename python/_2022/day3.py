import string
from python import utils


def get_priority(letter: str) -> int:
    if letter.islower():
        return string.ascii_lowercase.index(letter) + 1
    else:
        return string.ascii_uppercase.index(letter) + 27


def get_common_letter(*strings: str) -> str | None:
    first, *rest = strings
    for letter in first:
        if all(letter in other for other in rest):
            return letter


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day3")
    elves = input.split("\n")
    score = 0
    for elf in elves:
        middle = len(elf) // 2
        left, right = elf[:middle], elf[middle:]
        shared = get_common_letter(left, right)
        score += get_priority(shared)
    return score


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day3")
    elves = input.split("\n")
    score = 0
    for ii in range(0, len(elves), 3):
        elf, second, third = elves[ii : ii + 3]
        shared = get_common_letter(elf, second, third)
        score += get_priority(shared)
    return score


if __name__ == "__main__":
    assert part1() == 8233
    assert part2() == 2821
