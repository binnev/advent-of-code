from _2021.python import utils

raw = utils.load_puzzle_input("day6")


def init():
    return list(map(int, raw.split(",")))


@utils.profile
def part1():
    fishies = init()
    num_days = 80
    for day in range(num_days):
        fresh_fish = []
        for ii, fish in enumerate(fishies):
            if fish == 0:
                fishies[ii] = 6
                fresh_fish.append(8)
            else:
                fishies[ii] = fish - 1
        fishies.extend(fresh_fish)
    return len(fishies)


@utils.profile
def part2():
    initial_fishies = init()
    fishies = {ii: 0 for ii in range(9)}
    for fish in initial_fishies:
        fishies[fish] += 1

    for day in range(256):
        new_fishies = {ii: 0 for ii in range(9)}
        for days_till_spawn, count in fishies.items():
            if days_till_spawn == 0:
                new_fishies[8] += count
                new_fishies[6] += count
            else:
                new_fishies[days_till_spawn - 1] += count
        fishies = new_fishies
    return sum(fishies.values())


if __name__ == "__main__":
    assert part1() == 374927
    assert part2() == 1687617803407
