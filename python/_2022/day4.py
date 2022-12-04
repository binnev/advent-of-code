from python import utils

raw = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def parse_input() -> [[(int, int), (int, int)]]:
    input = utils.load_puzzle_input("2022/day4")
    rows = input.split("\n")
    elves = []
    for row in rows:
        str1, str2 = row.split(",")
        elf1 = tuple(map(int, str1.split("-")))
        elf2 = tuple(map(int, str2.split("-")))
        elves.append([elf1, elf2])
    return elves


def contains(s1, e1, s2, e2) -> bool:
    return (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2)


def overlaps(s1, e1, s2, e2) -> bool:
    return (e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)


@utils.profile
def part1():
    return sum(1 for elf1, elf2 in parse_input() if contains(*elf1, *elf2))


@utils.profile
def part2():
    return sum(1 for elf1, elf2 in parse_input() if overlaps(*elf1, *elf2))


if __name__ == "__main__":
    part1()
    part2()
