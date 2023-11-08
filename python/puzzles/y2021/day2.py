import utils


def process_input(raw: str):
    return list(map(str.strip, raw.strip().split("\n")))


@utils.profile
def part1(raw: str):
    instructions = process_input(raw)
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
def part2(raw: str):
    instructions = process_input(raw)
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
    raw = utils.load_puzzle_input("2021/day2")
    assert part1(raw) == 1451208
    assert part2(raw) == 1620141160
