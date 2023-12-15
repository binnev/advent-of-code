import utils


@utils.profile
def part1(input: str):
    steps = parse_input(input)
    return sum(map(hash, steps))


@utils.profile
def part2(input: str):
    ...


def hash(input: str) -> int:
    result = 0
    for char in input:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def parse_input(input: str) -> list[str]:
    # puzzle says to ignore newlines; better safe than sorry
    return input.strip().split(",")


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day15")
    part1(input)
