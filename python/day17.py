raw = "target area: x=143..177, y=-106..-71"
dummy = "target area: x=20..30, y=-10..-5"


raw = dummy


def init():
    target_x, target_y = raw.split(", ")
    target_x = target_x.split("x=")[-1]
    target_y = target_y.split("y=")[-1]
    min_x, max_x = map(int, target_x.split(".."))
    min_y, max_y = map(int, target_y.split(".."))
    print(min_x, max_x, min_y, max_y)
    target = dict()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            target[(x, y)] = "T"
            print(x, y)
    return target


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
    things = init()
    things[(0, 0)] = "S"
    positions, hit = calc_traj(5, 0, things)
    for p in positions:
        things[p] = "#"

    print_stuff(things)


if __name__ == "__main__":
    p1 = part1()
    print(f"{p1=}")
