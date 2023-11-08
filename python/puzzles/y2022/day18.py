import utils
from utils import SparseMatrix3, Coord3

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

LAVA = "█"
STEAM = "░"


def parse_input(raw: str) -> SparseMatrix3:
    grid = SparseMatrix3()

    for line in raw.splitlines():
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
    min_x, max_x = grid.get_xlim()
    min_y, max_y = grid.get_ylim()
    min_z, max_z = grid.get_zlim()

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


@utils.profile
def part1(raw: str):
    grid = parse_input(raw)
    surface_area = 0
    for cube in grid:
        for neighbour in get_3d_neighbours(cube):
            if not grid.get(neighbour):  # if face is exposed
                surface_area += 1
    return surface_area


@utils.profile
def part2(raw: str):
    grid = parse_input(raw)
    droplet = {pt: value for pt, value in grid.items() if value == LAVA}
    surround_with_steam(grid)
    surface_area = 0
    for cube in droplet:
        for neighbour in get_3d_neighbours(cube):
            if grid.get(neighbour) == STEAM:
                surface_area += 1
    return surface_area


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day18")
    assert part1(raw) == 4628
    assert part2(raw) == 2582
