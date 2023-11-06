import utils

example = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def find_marker(input: str, length: int) -> int:
    for ii in range(length, len(input)):
        snippet = input[ii - length : ii]
        if len(set(snippet)) == length:
            return ii


@utils.profile
def part1() -> int:
    input = utils.load_puzzle_input("2022/day6")
    return find_marker(input, length=4)


@utils.profile
def part2() -> int:
    input = utils.load_puzzle_input("2022/day6")
    return find_marker(input, length=14)


if __name__ == "__main__":
    assert part1() == 1175
    assert part2() == 3217
