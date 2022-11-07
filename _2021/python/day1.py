from _2021.python import utils

raw = utils.load_puzzle_input("day1")

input = list(map(int, map(str.strip, raw.strip().split("\n"))))


@utils.profile
def part1():
    increases = 0
    for ii, depth in enumerate(input):
        try:
            next_depth = input[ii + 1]
        except IndexError:
            pass  # reached end of list
        if next_depth > depth:
            increases += 1

    return increases


@utils.profile
def part2():
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
    assert part1() == 1482
    assert part2() == 1518
