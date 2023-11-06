from utils import load_puzzle_input, profile

puzzle_input = load_puzzle_input("2020/day2")


def parse_line(line: str) -> tuple[int, int, str, str]:
    policy, password = line.split(": ")
    numbers, letter = policy.split()
    a, b = map(int, numbers.split("-"))
    return a, b, letter, password


@profile
def part1():
    num_valid = 0
    for line in puzzle_input.split("\n"):
        _min, _max, letter, password = parse_line(line)
        if _min <= password.count(letter) <= _max:
            num_valid += 1
    return num_valid


@profile
def part2():
    num_valid = 0
    for line in puzzle_input.split("\n"):
        index1, index2, letter, password = parse_line(line)
        if (password[index1 - 1] == letter) ^ (password[index2 - 1] == letter):
            num_valid += 1
    return num_valid


if __name__ == "__main__":
    part1()
    part2()
