from python import utils

raw = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def contains(s1, e1, s2, e2) -> bool:
    """Does range 1 contain range 2"""
    return (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2)


def overlaps(s1, e1, s2, e2) -> bool:
    return (e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day4")
    rows = input.split("\n")
    score = 0
    for row in rows:
        elf1, elf2 = row.split(",")
        elf1_start, elf1_end = list(map(int, elf1.split("-")))
        elf2_start, elf2_end = list(map(int, elf2.split("-")))
        if contains(elf1_start, elf1_end, elf2_start, elf2_end):
            score += 1
    return score


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day4")
    rows = input.split("\n")
    score = 0
    for row in rows:
        elf1, elf2 = row.split(",")
        elf1_start, elf1_end = list(map(int, elf1.split("-")))
        elf2_start, elf2_end = list(map(int, elf2.split("-")))
        if overlaps(elf1_start, elf1_end, elf2_start, elf2_end):
            score += 1
    return score


if __name__ == "__main__":
    part1()
    part2()
