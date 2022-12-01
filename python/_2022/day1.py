from python import utils


def get_calories():
    raw = utils.load_puzzle_input("2022/day1")
    elves = raw.split("\n\n")
    return [sum(map(int, elf.split("\n"))) for elf in elves]


@utils.profile
def part1():
    return max(get_calories())


@utils.profile
def part2():
    return sum(sorted(get_calories(), reverse=True)[:3])


if __name__ == "__main__":
    assert part1() == 66186
    assert part2() == 196804
