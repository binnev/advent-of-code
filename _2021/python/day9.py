import numpy

from _2021.python import utils

raw = utils.load_puzzle_input("day9")


def init():
    return [list(map(int, row)) for row in raw.splitlines()]


def get_neighbours(input, x, y):
    neighbours = {}
    directions = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for x, y in directions:
        if x < 0 or y < 0:
            continue
        try:
            neighbours[(x, y)] = input[y][x]
        except IndexError:
            pass
    return neighbours


def find_low_points(input):
    low_points = []
    for y, row in enumerate(input):
        for x, cell in enumerate(row):
            neighbours = get_neighbours(input, x, y).values()
            if cell < min(neighbours):
                low_points.append((x, y))
    return low_points


@utils.profile
def part1():
    input = init()
    low_points = find_low_points(input)
    risk_level = 0
    for x, y in low_points:
        risk_level += int(input[y][x]) + 1
    return risk_level


def breadth_first_search(xy, input):
    """Each iteration
    1. get neighbours of current square
    2. add neighbours that are <= in height (add the coords)
    3. if the size of the collection didnt' change; break
    """
    x, y = xy
    basin = {(x, y)}
    while True:
        basin_size = len(basin)
        for x, y in basin:
            current_height = input[y][x]
            neighbours = get_neighbours(input, x, y)
            higher_neighbours = filter(lambda key: 9 > neighbours[key] > current_height, neighbours)
            basin = basin.union(higher_neighbours)
        # if basin didn't grow, we're done
        if len(basin) == basin_size:
            return basin


@utils.profile
def part2():
    """
    1. find lowest points
    2. find surrounding basins (breadth first search?)
    """
    input = init()
    low_points = find_low_points(input)
    basin_sizes = []
    for low_point in low_points:
        basin = breadth_first_search(low_point, input)
        basin_sizes.append(len(basin))
    return numpy.product(sorted(basin_sizes)[-3:])


if __name__ == "__main__":
    assert part1() == 522
    assert part2() == 916688
