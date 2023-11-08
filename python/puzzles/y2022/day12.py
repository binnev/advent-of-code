import math
import string
from typing import Callable

import numpy

import utils
from utils import Coord, SparseMatrix

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


def get_heightmap(input: str) -> tuple[SparseMatrix, Coord, Coord]:
    height_map = SparseMatrix()
    start, target = None, None
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            height_map[(x, y)] = get_height(char)
            if char == "S":
                start = (x, y)
            if char == "E":
                target = (x, y)
    return height_map, start, target


def get_neighbours(grid: SparseMatrix, pos: Coord, reverse: bool) -> list[Coord]:
    x, y = pos
    height = grid[pos]
    potential_neighbours = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    neighbours = []
    for n_pos in potential_neighbours:
        if n_pos not in grid:
            continue
        neighbour_height = grid[n_pos]
        condition = neighbour_height > height
        if reverse:
            condition = neighbour_height < height
        if condition:
            if abs(neighbour_height - height) < 2:
                neighbours.append(n_pos)
        else:
            neighbours.append(n_pos)
    return neighbours


def get_neighbours_uphill(grid: SparseMatrix, pos: Coord) -> list[Coord]:
    return get_neighbours(grid, pos, reverse=False)


def get_neighbours_downhill(grid: SparseMatrix, pos: Coord) -> list[Coord]:
    return get_neighbours(grid, pos, reverse=True)


def bfs(grid: SparseMatrix, start: Coord, get_neighbours_func: Callable) -> SparseMatrix:
    visited = set()
    frontier = [start]
    distances = SparseMatrix()
    distances[start] = 0
    neighbour_dist = 1
    while True:
        neighbours = set()  # new frontier
        for node in frontier:
            for neighbour in get_neighbours_func(grid, node):
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


def plot_grid(grid: SparseMatrix):
    import matplotlib.pyplot as plt

    xmin, xmax = grid.get_xlim()
    ymin, ymax = grid.get_ylim()
    width = xmax - xmin + 1
    height = ymax - ymin + 1
    arr = numpy.zeros((height, width))
    for (x, y), value in grid.items():
        arr[y][x] = value
    fig, ax = plt.subplots()
    ax.imshow(arr)
    plt.show()


@utils.profile
def part1(raw: str):
    grid, start, target = get_heightmap(raw)
    distances = bfs(grid, start=start, get_neighbours_func=get_neighbours_uphill)
    # plot_grid(SparseMatrix(distances))
    return distances[target]


@utils.profile
def part2(raw: str):
    """
    Flip it round; use the target as the start square, and find the distances of all points from
    that.
    """
    map, _, target = get_heightmap(raw)
    distances = bfs(map, start=target, get_neighbours_func=get_neighbours_downhill)

    low_points = []
    for coord, height in map.items():
        if height == 0:
            low_points.append(coord)

    results = []
    for pt in low_points:
        if pt in distances:
            results.append(distances[pt])
    return min(results)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day12")
    assert part1(raw) == 440
    assert part2(raw) == 439
