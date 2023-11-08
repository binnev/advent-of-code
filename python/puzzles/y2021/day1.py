import utils


def process_input(raw: str):
    return list(map(int, map(str.strip, raw.strip().split("\n"))))


@utils.profile
def part1(raw: str):
    input = process_input(raw)
    increases = 0
    previous_depth = 0
    for ii, depth in enumerate(input[1:]):
        if depth > previous_depth:
            increases += 1
        previous_depth = depth
    return increases


@utils.profile
def part2(raw: str):
    input = process_input(raw)
    increases = 0
    for ii, depth in enumerate(input):
        current_window = input[ii : ii + 3]
        next_window = input[ii + 1 : ii + 4]
        if len(next_window) < 3:
            break  # reached end of list
        if sum(next_window) > sum(current_window):
            increases += 1

    return increases


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day1")
    assert part1(raw) == 1482
    assert part2(raw) == 1518
