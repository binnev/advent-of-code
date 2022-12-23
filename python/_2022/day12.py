import math
import string
from typing import Callable

import numpy
from matplotlib.axes import Axes

from python import utils
from python.utils import Coord

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


Map = numpy.ndarray[numpy.ndarray[int]]


def get_height(char: str) -> int:
    if char == "S":
        char = "a"
    if char == "E":
        char = "z"
    return string.ascii_lowercase.index(char)


def get_heightmap(input: str) -> (Map, Coord, Coord):
    str_array = [list(line) for line in input.splitlines()]
    height_array = [[get_height(char) for char in line] for line in str_array]
    height_array = numpy.array(height_array)

    start, target = None, None
    for row, line in enumerate(str_array):
        for col, char in enumerate(line):
            if char == "S":
                start = (col, row)
            if char == "E":
                target = (col, row)
    return height_array, start, target


def get_neighbours(map: Map, pos: Coord) -> list[Coord]:
    x, y = pos
    height = map[y][x]
    potential_neighbours = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    neighbours = []
    for nx, ny in potential_neighbours:
        if nx < 0 or ny < 0:
            continue
        try:
            neighbour_height = map[ny][nx]
            if neighbour_height > height:
                if abs(neighbour_height - height) < 2:
                    neighbours.append((nx, ny))
            else:  # lower neighbours always OK
                neighbours.append((nx, ny))
        except IndexError:
            continue  # outside map
    return neighbours


def get_neighbours_reversed(map: Map, pos: Coord) -> list[Coord]:
    """
    Get neighbours following the same rules, but when travelling downwards instead of upwards
    """

    x, y = pos
    height = map[y][x]
    potential_neighbours = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    neighbours = []
    for nx, ny in potential_neighbours:
        if nx < 0 or ny < 0:
            continue
        try:
            neighbour_height = map[ny][nx]
            if neighbour_height < height:
                if abs(neighbour_height - height) < 2:
                    neighbours.append((nx, ny))
            else:  # lower neighbours always OK
                neighbours.append((nx, ny))
        except IndexError:
            continue  # outside map
    return neighbours


def bfs(map: Map, start: Coord, get_neighbours_func: Callable) -> dict[Coord:int]:
    """
    PLAN:
    - convert the map to a graph (create links between every node if the height diff < 2)
    - run Dijkstra
        - iteration 1
        - pick starting node. Find the distance to all its neighbours
        - update those neighbour nodes with their distance from starting pt
        - move starting node into the "visited" array

        - iteration 2
        - pick new node -- the one with the smallest distance from the start
        - etc


        We will end up with an array of distances for each node.
        But what about the path? All we need is the distance.
    """

    visited = set()
    frontier = [start]
    distances = {start: 0}
    neighbour_dist = 1
    while True:
        neighbours = set()  # new frontier
        for node in frontier:
            for neighbour in get_neighbours_func(map, node):
                if neighbour not in visited:
                    neighbours.add(neighbour)

        if not neighbours:
            break  # finished because explored whole map (hopefully...)

        for n in neighbours:
            dist = min(distances.get(n, math.inf), neighbour_dist)
            distances[n] = dist

        visited = visited.union(frontier)
        frontier = neighbours
        neighbour_dist += 1

    return distances


def plot_map(map: Map):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax: Axes
    ax.imshow(map)
    plt.show()


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day12")
    map, start, target = get_heightmap(input)
    distances = bfs(map, start=start, get_neighbours_func=get_neighbours)
    # plot_map(map)
    # distances_img = numpy.ones(map.shape) * math.inf
    # for (x, y), dist in distances.items():
    #     distances_img[y][x] = dist
    #
    # plot_map(distances_img)
    return distances[target]


@utils.profile
def part2():
    """
    Flip it round; use the target as the start square, and find the distances of all points from
    that.
    """
    input = utils.load_puzzle_input("2022/day12")
    map, _, target = get_heightmap(input)
    distances = bfs(map, start=target, get_neighbours_func=get_neighbours_reversed)

    low_points = []
    for y, row in enumerate(map):
        for x, height in enumerate(row):
            if height == 0:
                low_points.append((x, y))

    results = []
    for pt in low_points:
        if pt in distances:
            results.append(distances[pt])
    return min(results)


if __name__ == "__main__":
    assert part1() == 440
    assert part2() == 439
