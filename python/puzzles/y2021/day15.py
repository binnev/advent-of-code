import math
import utils


def init(raw: str):
    return {
        (x, y): int(cell) for y, row in enumerate(raw.splitlines()) for x, cell in enumerate(row)
    }


def init2(raw: str):
    repeats = 5
    cave = init(raw)
    new_cave = dict()
    width = max([x for x, y in cave]) + 1
    height = max([y for x, y in cave]) + 1

    for (x, y), value in cave.items():
        for ii in range(repeats):  # x
            for jj in range(repeats):  # y
                new_value = max((value + ii + jj) % 9, (value + ii + jj) % 10)
                new_coords = (x + width * ii, y + height * jj)
                new_cave[new_coords] = new_value
    return new_cave


def print_cave(cave):
    max_x = max([x for x, y in cave]) + 1
    max_y = max([y for x, y in cave]) + 1
    for y in range(max_y):
        for x in range(max_x):
            print(cave[(x, y)], end="")
        print("")


def get_neighbours(cave, x, y):
    directions = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
    neighbours = {(x, y): cave[(x, y)] for (x, y) in directions if (x, y) in cave}
    return neighbours


def dijkstra(cave):
    spt = dict()  # shortest path tree
    distances = {(0, 0): 0}
    max_x = max([x for x, y in cave])
    max_y = max([y for x, y in cave])
    finish = (max_x, max_y)
    while finish not in spt:
        # choose node from distances with the lowest distance. Add that to spt
        node = min(distances, key=lambda key: distances[key])
        spt[node] = distances.pop(node)

        # update the distances of the nodes adjacent to the new node
        neighbours = get_neighbours(cave, *node)
        for neighbour, risk in neighbours.items():
            # filter out ones that are already in spt
            if neighbour in spt:
                continue

            # update distances: distance of current node PLUS the adjacent node's cave value
            # keep whichever one is smaller
            distances[neighbour] = min(distances.get(neighbour, math.inf), spt[node] + risk)

    return spt[finish]


@utils.profile
def part1(raw: str):
    cave = init(raw)
    shortest_path = dijkstra(cave)
    return shortest_path


@utils.profile
def part2(raw: str):
    cave = init2(raw)
    shortest_path = dijkstra(cave)
    return shortest_path


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day15")
    assert part1(raw) == 423
    assert part2(raw) == 2778
