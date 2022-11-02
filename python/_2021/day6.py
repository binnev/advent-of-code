raw = """3,5,4,1,2,1,5,5,1,1,1,1,4,1,4,5,4,5,1,3,1,1,1,4,1,1,3,1,1,5,3,1,1,3,1,3,1,1,1,4,1,2,5,3,1,4,2,3,1,1,2,1,1,1,4,1,1,1,1,2,1,1,1,3,1,1,4,1,4,1,5,1,4,2,1,1,5,4,4,4,1,4,1,1,1,1,3,1,5,1,4,5,3,1,4,1,5,2,2,5,1,3,2,2,5,4,2,3,4,1,2,1,1,2,1,1,5,4,1,1,1,1,3,1,5,4,1,5,1,1,4,3,4,3,1,5,1,1,2,1,1,5,3,1,1,1,1,1,5,1,1,1,1,1,1,1,2,2,5,5,1,2,1,2,1,1,5,1,3,1,5,2,1,4,1,5,3,1,1,1,2,1,3,1,4,4,1,1,5,1,1,4,1,4,2,3,5,2,5,1,3,1,2,1,4,1,1,1,1,2,1,4,1,3,4,1,1,1,1,1,1,1,2,1,5,1,1,1,1,2,3,1,1,2,3,1,1,3,1,1,3,1,3,1,3,3,1,1,2,1,3,2,3,1,1,3,5,1,1,5,5,1,2,1,2,2,1,1,1,5,3,1,1,3,5,1,3,1,5,3,4,2,3,2,1,3,1,1,3,4,2,1,1,3,1,1,1,1,1,1"""


def init():
    return list(map(int, raw.split(",")))


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
    print(f"part1: {part1()}")
    print(f"part2: {part2()}")
