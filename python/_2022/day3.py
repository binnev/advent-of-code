import string
from python import utils

raw = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

PRIORITIES = {}
for ii, letter in enumerate(string.ascii_lowercase, start=1):
    PRIORITIES[letter] = ii
for ii, letter in enumerate(string.ascii_uppercase, start=27):
    PRIORITIES[letter] = ii


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day3")
    rucksacks = input.split("\n")
    priorities = 0
    for rucksack in rucksacks:
        left = set(rucksack[: len(rucksack) // 2])
        right = set(rucksack[len(rucksack) // 2 :])
        shared = left.intersection(right)
        priorities += PRIORITIES[shared.pop()]
    return priorities


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day3")
    elves = input.split("\n")
    score = 0
    for ii in range(0, len(elves), 3):
        try:
            elf, second, third = elves[ii], elves[ii + 1], elves[ii + 2]
        except IndexError:
            pass  # end of list
        letters = set(elf + second + third)
        shared = next(
            letter for letter in letters if letter in elf and letter in second and letter in third
        )
        score += PRIORITIES[shared]
        ii += 3
    return score


if __name__ == "__main__":
    part1()
    part2()
