import utils


def get_calories(raw: str):
    elves = raw.split("\n\n")
    return [sum(map(int, elf.split("\n"))) for elf in elves]


@utils.profile
def part1(raw: str):
    return max(get_calories(raw))


@utils.profile
def part2(raw: str):
    return sum(sorted(get_calories(raw), reverse=True)[:3])


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day1")
    assert part1(raw) == 66186
    assert part2(raw) == 196804
