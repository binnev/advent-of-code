import utils
from utils import SparseMatrix, Coord

example = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

smaller_example = """.....
..##.
..#..
.....
..##.
....."""

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3
DIRECTION_NAMES = {NORTH: "NORTH", EAST: "EAST", SOUTH: "SOUTH", WEST: "WEST"}


class BadDirection(ValueError):
    def __init__(self, direction: int):
        super().__init__(f"Bad direction: {direction}")


def get_directions(pos: Coord) -> list[Coord]:
    x, y = pos
    return [
        (x, y - 1),  # north
        (x, y + 1),  # south
        (x - 1, y),  # west
        (x + 1, y),  # east
    ]


def get_surrounding(pos: Coord) -> list[Coord]:
    x, y = pos
    return get_directions(pos) + [
        (x + 1, y + 1),  # southeast
        (x + 1, y - 1),  # northeast
        (x - 1, y + 1),  # southwest
        (x - 1, y - 1),  # northwest
    ]


def get_neighbours(pos: Coord, direction: int) -> list[Coord]:
    x, y = pos
    if direction == NORTH:
        new_y = y - 1
        neighbours = [(x, new_y), (x - 1, new_y), (x + 1, new_y)]
    elif direction == SOUTH:
        new_y = y + 1
        neighbours = [(x, new_y), (x - 1, new_y), (x + 1, new_y)]
    elif direction == EAST:
        new_x = x + 1
        neighbours = [(new_x, y), (new_x, y + 1), (new_x, y - 1)]
    elif direction == WEST:
        new_x = x - 1
        neighbours = [(new_x, y), (new_x, y + 1), (new_x, y - 1)]
    else:
        raise BadDirection(direction)
    return neighbours


def parse_input(input: str) -> SparseMatrix:
    grid = SparseMatrix()
    for y, line in enumerate(input.splitlines()):
        for x, value in enumerate(line):
            if value == "#":
                grid[(x, y)] = value
    return grid


def get_next_square(pos: Coord, direction: int) -> Coord:
    x, y = pos
    if direction == NORTH:
        new_square = (x, y - 1)
    elif direction == SOUTH:
        new_square = (x, y + 1)
    elif direction == EAST:
        new_square = (x + 1, y)
    elif direction == WEST:
        new_square = (x - 1, y)
    else:
        raise BadDirection(direction)
    return new_square


def empty_ground(grid: SparseMatrix) -> int:
    min_x, max_x = grid.get_xlim()
    min_y, max_y = grid.get_ylim()
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    area = width * height
    return area - len(grid)


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day23")
    grid = parse_input(input)

    direction_counter = NORTH
    for iteration in range(10):
        proposals = dict[Coord, list[Coord]]()
        # 1) propose move for each elf
        for elf in grid:
            surroundings = get_surrounding(elf)
            if not any(grid.get(pt) for pt in surroundings):
                continue  # elf is already properly placed; it does nothing

            for ii in range(4):
                direction = (direction_counter + ii) % 4
                neighbours = get_neighbours(elf, direction)
                if not any(grid.get(pt) for pt in neighbours):
                    new_square = get_next_square(elf, direction)
                    proposals[new_square] = proposals.get(new_square, []) + [elf]
                    break

        # 2) move each elf if possible -- if they're the only elf proposing that sq.
        for next_square, elves in proposals.items():
            if len(elves) == 1:
                elf = elves[0]
                grid[next_square] = grid.pop(elf)

        direction_counter = (direction_counter + 1) % 4
        if not proposals:
            break
    return empty_ground(grid)


@utils.profile
def part2():
    # input = example
    input = utils.load_puzzle_input("2022/day23")
    grid = parse_input(input)

    direction_counter = NORTH
    iteration = 0
    proposals = True
    while proposals:
        proposals = dict[Coord, list[Coord]]()
        # 1) propose move for each elf
        for elf in grid:
            surroundings = get_surrounding(elf)
            if not any(grid.get(pt) for pt in surroundings):
                continue  # elf is already properly placed; it does nothing

            for ii in range(4):
                direction = (direction_counter + ii) % 4
                neighbours = get_neighbours(elf, direction)
                if not any(grid.get(pt) for pt in neighbours):
                    new_square = get_next_square(elf, direction)
                    proposals[new_square] = proposals.get(new_square, []) + [elf]
                    break

        # 2) move each elf if possible -- if they're the only elf proposing that sq.
        for next_square, elves in proposals.items():
            if len(elves) == 1:
                elf = elves[0]
                grid[next_square] = grid.pop(elf)

        direction_counter = (direction_counter + 1) % 4
        iteration += 1
        if not proposals:
            break
    grid.print()
    return iteration


if __name__ == "__main__":
    assert part1() == 4236
    assert part2() == 1023
