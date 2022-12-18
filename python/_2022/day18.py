import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from python import utils
from python._2022.day14 import print_sparse_matrix

example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

Coord3 = tuple[int, int, int]
SparseMatrix3 = dict[Coord3, str]
LAVA = "░"
STEAM = "s"


def parse_input(input: str) -> SparseMatrix3:
    grid = SparseMatrix3()

    for line in input.splitlines():
        point = tuple(map(int, line.split(",")))
        grid[point] = LAVA
    return grid


def get_3d_neighbours(cube: Coord3) -> list[Coord3]:
    x, y, z = cube
    neighbours = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    return neighbours


def surround_with_steam(grid: SparseMatrix3):
    """
    Surround the lava droplet with a BFS-grown steam cube
    """
    min_x = min(x for x, y, z in grid)
    max_x = max(x for x, y, z in grid)
    min_y = min(y for x, y, z in grid)
    max_y = max(y for x, y, z in grid)
    min_z = min(z for x, y, z in grid)
    max_z = max(z for x, y, z in grid)

    steam_min_x = min_x - 1
    steam_max_x = max_x + 1
    steam_min_y = min_y - 1
    steam_max_y = max_y + 1
    steam_min_z = min_z - 1
    steam_max_z = max_z + 1
    visited = set()
    start = (steam_min_x, steam_min_y, steam_min_z)
    frontier = [start]
    grid[start] = STEAM
    while True:
        neighbours = set()
        for node in frontier:
            for neighbour in get_3d_neighbours(node):
                if (
                    neighbour not in visited
                    and neighbour not in grid
                    and steam_min_x <= neighbour[0] <= steam_max_x
                    and steam_min_y <= neighbour[1] <= steam_max_y
                    and steam_min_z <= neighbour[2] <= steam_max_z
                ):
                    neighbours.add(neighbour)

        if not neighbours:
            break

        for n in neighbours:
            grid[n] = STEAM

        visited = visited.union(frontier)
        frontier = neighbours


def plot_droplet(grid: SparseMatrix3):
    min_x = min(x for x, y, z in grid)
    max_x = max(x for x, y, z in grid)
    min_y = min(y for x, y, z in grid)
    max_y = max(y for x, y, z in grid)
    min_z = min(z for x, y, z in grid)
    max_z = max(z for x, y, z in grid)
    x_width = max_x - min_x + 1
    y_width = max_y - min_y + 1
    z_width = max_z - min_z + 1
    filled = np.zeros((x_width, y_width, z_width), dtype=bool)
    for x, y, z in grid:
        filled[x][y][z] = True

    ax: Axes3D = plt.figure().add_subplot(projection="3d")
    ax.voxels(
        filled,
        facecolors=[1, 0, 0, 0.1],
    )
    ax.set_aspect("equal")
    plt.show()


def print_sparse_matrix_3d(grid: SparseMatrix3):
    min_z = min(z for x, y, z in grid)
    max_z = max(z for x, y, z in grid)
    for layer_z in range(min_z, max_z + 1):
        layer = {(x, y): value for (x, y, z), value in grid.items() if z == layer_z}
        print_sparse_matrix(layer, pad=2)


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day18")
    grid = parse_input(input)

    surface_area = 0
    for cube in grid:
        for neighbour in get_3d_neighbours(cube):
            if not grid.get(neighbour):  # if face is exposed
                surface_area += 1
    return surface_area


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day18")
    grid = parse_input(input)
    droplet = {pt: value for pt, value in grid.items() if value == LAVA}
    surround_with_steam(grid)
    surface_area = 0
    for cube in droplet:
        for neighbour in get_3d_neighbours(cube):
            if grid.get(neighbour) == STEAM:
                surface_area += 1
    return surface_area


if __name__ == "__main__":
    assert part1() == 4628
    assert part2() == 2582
