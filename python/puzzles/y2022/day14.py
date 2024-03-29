import utils
from utils import SparseMatrix, Coord

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

FALLING = 0
RESTING = 1
DESTROYED = 2
WALL = "█"
SAND = "░"


def draw_line(start: Coord, end: Coord, grid: SparseMatrix):
    start_x, start_y = start
    end_x, end_y = end
    dy = end_y - start_y
    start_x, end_x = min(start_x, end_x), max(start_x, end_x)
    start_y, end_y = min(start_y, end_y), max(start_y, end_y)

    if dy == 0:
        for x in range(start_x, end_x + 1):
            grid[(x, start_y)] = WALL
    else:
        for y in range(start_y, end_y + 1):
            grid[(start_x, y)] = WALL


def parse_input(raw: str) -> SparseMatrix:
    instructions = raw.splitlines()
    grid = SparseMatrix()
    for ins in instructions:
        points = [tuple(map(int, pair.split(","))) for pair in ins.split(" -> ")]
        for ii in range(len(points) - 1):
            start = points[ii]
            end = points[ii + 1]
            draw_line(start, end, grid)
    return grid


def sand_step(pos: Coord, grid: SparseMatrix, floor: int, solid_floor: bool) -> tuple[Coord, int]:
    x, y = pos
    options = [
        (x, y + 1),  # down
        (x - 1, y + 1),  # down_left
        (x + 1, y + 1),  # down_right
    ]
    for x, y in options:
        if (x, y) not in grid:
            if y == floor:
                if solid_floor:
                    return pos, RESTING
                else:
                    return pos, DESTROYED
            else:
                return (x, y), FALLING

    # all movement options blocked; sand came to rest on obstacle
    return pos, RESTING


def sand_trace(origin: Coord, grid: SparseMatrix, floor: int, solid_floor: bool) -> int:
    pos = origin

    status = FALLING
    while status == FALLING:
        new_pos, status = sand_step(pos, grid, floor, solid_floor)
        pos = new_pos

    if status == RESTING:
        grid[pos] = SAND
    return status


@utils.profile
def part1(raw: str):
    grid = parse_input(raw)
    origin = (500, 0)
    floor = max(y for x, y in grid)
    ii = 0
    while True:
        status = sand_trace(origin, grid, floor=floor, solid_floor=False)
        if status == DESTROYED:
            break
        ii += 1
    return ii


@utils.profile
def part2(raw: str):
    # todo: speed this up by ignoring any sand particles that get further left/right than the l/r
    #  bounds of the platforms.
    grid = parse_input(raw)
    origin = (500, 0)
    floor = 2 + max(y for x, y in grid)
    ii = 0
    while True:
        sand_trace(origin, grid, floor=floor, solid_floor=True)
        ii += 1
        if origin in grid:
            break
    return ii


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day14")
    assert part1(raw) == 755
    assert part2(raw) == 29805
