from python import utils
from python._2022.day14 import SparseMatrix

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


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day18")
    grid = SparseMatrix()

    for line in input.splitlines():
        point = tuple(map(int, line.split(",")))
        grid[point] = "#"

    surface_area = 0
    for cube in grid:
        for neighbour in get_3d_neighbours(cube):
            if not grid.get(neighbour):  # if face is exposed
                surface_area += 1

    return surface_area


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
