import utils

example = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def find_marker(input: str, length: int) -> int:
    for ii in range(length, len(input)):
        snippet = input[ii - length : ii]
        if len(set(snippet)) == length:
            return ii


@utils.profile
def part1(raw: str) -> int:
    return find_marker(raw, length=4)


@utils.profile
def part2(raw: str) -> int:
    return find_marker(raw, length=14)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day6")
    assert part1(raw) == 1175
    assert part2(raw) == 3217
