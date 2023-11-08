import utils


School = dict[int:int]


def init(raw: str) -> School:
    fish = list(map(int, raw.split(",")))
    school: School = {n: fish.count(n) for n in range(9)}
    return school


def iterate_fish(fish: School):
    new_fishies = {ii: 0 for ii in range(9)}
    for days_till_spawn, count in fish.items():
        if days_till_spawn == 0:
            new_fishies[8] += count
            new_fishies[6] += count
        else:
            new_fishies[days_till_spawn - 1] += count
    return new_fishies


@utils.profile
def part1(raw: str):
    fishies = init(raw)
    for _ in range(80):
        fishies = iterate_fish(fishies)
    return sum(fishies.values())


@utils.profile
def part2(raw: str):
    fishies = init(raw)
    for _ in range(256):
        fishies = iterate_fish(fishies)
    return sum(fishies.values())


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day6")
    assert part1(raw) == 374927
    assert part2(raw) == 1687617803407
