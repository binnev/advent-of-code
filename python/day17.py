raw = "target area: x=143..177, y=-106..-71"
dummy = "target area: x=20..30, y=-10..-5"


raw = dummy


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
    # 1) calibrate x
    hit = False
    u0 = 1
    v0 = 1
    while not hit:
        print(f"trying u0={u0}, v0=0")
        positions, _ = calc_traj(u0, v0, things)
        final_pos = positions[-1]
        hit = final_pos[0] in target_x
        for p in positions:
            things[p] = "#"
        if hit: break
        u0 += 1
        v0 += 1

    hit = False
    v0 = 1
    while True:
        print(f"trying u0={u0}, v0={v0+1}")
        positions, hit = calc_traj(u0, v0 + 1, things)
        for p in positions:
            things[p] = "#"
        if not hit:
            break  # v0 was the last one to hit
        v0 += 1

    # print_stuff(things)
    max_y = max([y for x, y in positions])
    return max_y


if __name__ == "__main__":
    p1 = part1()
    print(f"{p1=}")
