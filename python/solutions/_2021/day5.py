import utils


raw = utils.load_puzzle_input("2021/day5")


def init():
    lines = raw.splitlines()
    output = [
        [tuple(map(int, coords.split(","))) for coords in line.split(" -> ")] for line in lines
    ]
    size = max(coord for row in output for pair in row for coord in pair) + 1
    return output, size


def do_the_thing(skip_diagonals=True):
    coords, size = init()
    sparse_matrix = dict()
    for (x1, y1), (x2, y2) in coords:
        if skip_diagonals and (x1 != x2) and (y1 != y2):
            continue
        x, y = x1, y1
        while True:
            sparse_matrix[(x, y)] = sparse_matrix.get((x, y), 0) + 1
            if x == x2 and y == y2:
                break
            if x != x2:
                x += 1 if x < x2 else -1
            if y != y2:
                y += 1 if y < y2 else -1

    return sum(1 for value in sparse_matrix.values() if value > 1)


@utils.profile
def part1():
    return do_the_thing()


@utils.profile
def part2():
    return do_the_thing(skip_diagonals=False)


if __name__ == "__main__":
    assert part1() == 7644
    assert part2() == 18627
