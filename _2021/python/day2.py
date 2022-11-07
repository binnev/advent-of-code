from _2021.python import utils

raw = utils.load_puzzle_input("day2")


instructions = list(map(str.strip, raw.strip().split("\n")))


@utils.profile
def part1():
    depth = 0
    horizontal = 0

    for instruction in instructions:
        direction, magnitude = instruction.split()
        magnitude = int(magnitude)
        if direction == "forward":
            horizontal += magnitude
        elif direction == "up":
            depth -= magnitude
        elif direction == "down":
            depth += magnitude
        else:
            raise Exception(f"unknown direction {direction}")
    return depth * horizontal


@utils.profile
def part2():
    depth = 0
    horizontal = 0
    aim = 0

    for instruction in instructions:
        direction, magnitude = instruction.split()
        magnitude = int(magnitude)
        if direction == "forward":
            horizontal += magnitude
            depth += magnitude * aim
        elif direction == "up":
            aim -= magnitude
        elif direction == "down":
            aim += magnitude
        else:
            raise Exception(f"unknown direction {direction}")
    return depth * horizontal


if __name__ == "__main__":
    assert part1() == 1451208
    assert part2() == 1620141160
