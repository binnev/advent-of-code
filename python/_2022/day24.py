from typing import Literal, NamedTuple, Iterable

import numpy

from python import utils
from python._2022.day23 import get_next_square
from python.utils import SparseMatrix, Coord

example = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

larger_example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3
Heading = Literal[0, 1, 2, 3]
HEADING_NAMES = {
    NORTH: "NORTH",
    EAST: "EAST",
    SOUTH: "SOUTH",
    WEST: "WEST",
}
ARROW_TO_HEADING = {
    "^": NORTH,
    ">": EAST,
    "v": SOUTH,
    "<": WEST,
}
HEADING_TO_ARROW = {v: k for k, v in ARROW_TO_HEADING.items()}
NUMBER_TO_BLIZZARD = {
    1: "░",
    2: "▒",
    3: "▓",
    4: "█",
}
BLIZZARD_TO_NUMBER = {v: k for k, v in NUMBER_TO_BLIZZARD.items()}
WALL = "#"
EMPTY = " "
ELF = "░"
ELF = "▒"
ELF = "▓"
ELF = "█"
ELF = "e"

Blizzards = dict[int, tuple[Coord, Heading]]
Map = numpy.ndarray[numpy.ndarray[str]]


class State(NamedTuple):
    minute: int  # minutes elapsed
    pos: Coord  # current position


def parse_input(input: str) -> (SparseMatrix, Blizzards):
    blizzards = Blizzards()
    grid = SparseMatrix()
    blizz_id = 0
    for y, line in enumerate(input.splitlines()):
        for x, value in enumerate(line):
            if value == "#":
                grid[(x, y)] = WALL
            elif value in ["<", ">", "^", "v"]:
                heading = ARROW_TO_HEADING[value]
                blizzards[blizz_id] = ((x, y), heading)
                blizz_id += 1
                grid[(x, y)] = EMPTY
            else:
                grid[(x, y)] = EMPTY
    return grid, blizzards


def print_sparse(grid: SparseMatrix, blizzards: Blizzards, elves: set[Coord]):
    grid = SparseMatrix({**grid})
    for id, (pos, heading) in blizzards.items():
        if pos not in grid or grid[pos] == EMPTY:
            grid[pos] = NUMBER_TO_BLIZZARD[1]
        else:
            blizz = grid[pos]
            intensity = BLIZZARD_TO_NUMBER[blizz]
            intensity += 1
            blizz = NUMBER_TO_BLIZZARD[intensity]
            grid[pos] = str(blizz)
    for elf in elves:
        grid[elf] = ELF
    grid.print()


def pacman_wrap(pos: Coord, heading: int, grid: SparseMatrix) -> Coord:
    """
    Teleport to the opposite side of the world a la Pacman.
    """
    current_x, current_y = pos
    if heading == EAST:
        next_x = min(x for (x, y), value in grid.items() if y == current_y and value == EMPTY)
        next_square = (next_x, current_y)
    elif heading == WEST:
        next_x = max(x for (x, y), value in grid.items() if y == current_y and value == EMPTY)
        next_square = (next_x, current_y)
    elif heading == NORTH:
        next_y = max(y for (x, y), value in grid.items() if x == current_x and value == EMPTY)
        next_square = (current_x, next_y)
    elif heading == SOUTH:
        next_y = min(y for (x, y), value in grid.items() if x == current_x and value == EMPTY)
        next_square = (current_x, next_y)
    else:
        raise ValueError(f"Bad direction: {heading}")
    return next_square


def iterate_blizzards(grid: SparseMatrix, blizzards: Blizzards):
    for id, (pos, heading) in blizzards.items():
        new_pos = get_next_square(pos, heading)
        if new_pos not in grid or grid[new_pos] == WALL:
            new_pos = pacman_wrap(pos, heading, grid)
            blizzards[id] = (new_pos, heading)
        else:
            blizzards[id] = (new_pos, heading)


def get_neighbouring_squares(pos: Coord) -> list[Coord]:
    x, y = pos
    return [
        (x, y - 1),  # north
        (x, y + 1),  # south
        (x - 1, y),  # west
        (x + 1, y),  # east
    ]


def get_options(pos: Coord, grid: SparseMatrix, blizzards: Blizzards) -> set[Coord]:
    elves = set()
    # get neighbouring squares in all N/S/E/W directions. Only consider those that are not
    # blocked by a wall or a blizzard.
    for coord in get_neighbouring_squares(pos):
        if coord not in grid or grid[coord] == WALL:
            continue
        # if any(blizzard_coord == coord for id, (blizzard_coord, _) in blizzards.items()):
        #     continue
        elves.add(coord)
    return elves


def draw_blizzards_on_grid(grid: SparseMatrix, blizzards: Blizzards):
    for id, (coord, heading) in blizzards.items():
        arrow = HEADING_TO_ARROW[heading]
        grid[coord] = arrow


def run_the_gauntlet(
    start: Coord,
    target: Coord,
    grid: SparseMatrix,
    blizzards: Blizzards,
) -> int:
    elves = {start}
    minute = 0
    while True:
        for elf in elves:
            options = get_options(elf, grid, blizzards)
            elves = elves.union(options)
        iterate_blizzards(grid, blizzards)
        # handle death by blizzard collision
        for id, (coord, heading) in blizzards.items():
            if coord in elves:
                elves.remove(coord)
        minute += 1
        if any(elf == target for elf in elves):
            break
    return minute


@utils.profile
def part1():
    # input = larger_example
    input = utils.load_puzzle_input("2022/day24")
    grid, blizzards = parse_input(input)
    START = (1, 0)
    target_y = max(y for x, y in grid)
    TARGET = next((x, y) for (x, y), value in grid.items() if y == target_y and value == EMPTY)
    return run_the_gauntlet(start=START, target=TARGET, grid=grid, blizzards=blizzards)


@utils.profile
def part2():
    # input = larger_example
    input = utils.load_puzzle_input("2022/day24")
    grid, blizzards = parse_input(input)
    START = (1, 0)
    target_y = max(y for x, y in grid)
    TARGET = next((x, y) for (x, y), value in grid.items() if y == target_y and value == EMPTY)
    minute = 0
    minute += run_the_gauntlet(start=START, target=TARGET, grid=grid, blizzards=blizzards)
    minute += run_the_gauntlet(start=TARGET, target=START, grid=grid, blizzards=blizzards)
    minute += run_the_gauntlet(start=START, target=TARGET, grid=grid, blizzards=blizzards)
    return minute


if __name__ == "__main__":
    assert part1() == 228
    assert part2() == 723
