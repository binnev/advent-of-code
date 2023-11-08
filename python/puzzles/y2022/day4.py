import utils

ElfRange = (int, int)


def parse_input(raw: str) -> list[list[ElfRange, ElfRange]]:
    rows = raw.split("\n")
    elves = []
    for row in rows:
        str1, str2 = row.split(",")
        elf1 = tuple(map(int, str1.split("-")))
        elf2 = tuple(map(int, str2.split("-")))
        elves.append([elf1, elf2])
    return elves


def contains(range1: ElfRange, range2: ElfRange) -> bool:
    (s1, e1), (s2, e2) = range1, range2
    return (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2)


def overlaps(range1: ElfRange, range2: ElfRange) -> bool:
    (s1, e1), (s2, e2) = range1, range2
    return (e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)


@utils.profile
def part1(raw: str):
    # abusing the fact that True == 1 and False == 0 for style points (or maybe negative style
    # points; you decide...)
    return sum(contains(elf1, elf2) for elf1, elf2 in parse_input(raw))


@utils.profile
def part2(raw: str):
    return sum(overlaps(elf1, elf2) for elf1, elf2 in parse_input(raw))


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day4")
    assert part1(raw) == 567
    assert part2(raw) == 907
