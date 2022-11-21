from python import utils

raw = utils.load_puzzle_input("2021/day17")


def init():
    target_x, target_y = raw.split(", ")
    target_x = target_x.split("x=")[-1]
    target_y = target_y.split("y=")[-1]
    min_x, max_x = map(int, target_x.split(".."))
    min_y, max_y = map(int, target_y.split(".."))
    target = dict()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            target[(x, y)] = "T"
    return target, range(min_x, max_x + 1), range(min_y, max_y + 1)


def print_stuff(things):
    xs = [x for x, y in things]
    ys = [-y for x, y in things]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(things.get((x, -y), "."), end="")
        print("")


def calc_traj(u, v, target_x, target_y):
    x = 0
    y = 0
    positions = []
    while True:
        x += u
        y += v
        positions.append((x, y))
        if u != 0:
            u += -1 if u > 0 else 1
        v -= 1
        if x in target_x and y in target_y:
            return positions, True
        if y < target_y.start:
            return positions, False

@utils.profile
def part1():
    """
    x and y are totally independent!
    find the u range that ends in the target x
    ditto for v
    then search that space
        :return:
    """
    things, target_x, target_y = init()
    things[(0, 0)] = "S"

    def calc_traj(u, v, things):
        x = 0
        y = 0
        positions = []
        min_y = min(y for (x, y), code in things.items() if code == "T")
        while True:
            x += u
            y += v
            positions.append((x, y))
            if u != 0:
                u += -1 if u > 0 else 1
            v -= 1
            if things.get((x, y)) == "T":
                return positions, True
            if y < min_y:
                return positions, False

    trajectories = []
    for u0 in range(200):
        for v0 in range(200):
            positions, hit = calc_traj(u0, v0, things)
            if hit:
                trajectories.append(positions)

    return max(y for traj in trajectories for x, y in traj)

@utils.profile
def part2():
    """
    x and y are totally independent!
    find the u range that ends in the target x
    ditto for v
    then search that space
        :return:
    """
    things, target_x, target_y = init()
    things[(0, 0)] = "S"

    trajectories = []
    for u0 in range(250):
        for v0 in range(-150, 250):
            positions, hit = calc_traj(u0, v0, target_x, target_y)
            if hit:
                trajectories.append(positions)

    return len(trajectories)


"""New idea: get all trajectories that _cross_ the target (including diagonally) """


if __name__ == "__main__":
    assert part1() == 5565
    assert part2() == 2118
