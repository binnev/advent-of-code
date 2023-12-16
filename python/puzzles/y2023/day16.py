import enum
from typing import NamedTuple

import utils
from utils import SparseMatrix, Coord

EMPTY = "."
SPLITTERS = "|-"
MIRRORS = r"\/"


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


DIRECTION_STR = {
    Direction.LEFT: "<",
    Direction.RIGHT: ">",
    Direction.UP: "^",
    Direction.DOWN: "v",
}


class Beam(NamedTuple):
    coord: Coord
    direction: Direction


@utils.profile
def part1(input: str):
    matrix = parse_input(input)
    return trace_beam(matrix)


@utils.profile
def part2(input: str):
    matrix = parse_input(input)
    xmin, xmax = matrix.get_xlim()
    ymin, ymax = matrix.get_ylim()
    results = []
    print("doing horizontal beams...")
    for x in range(xmin, xmax + 1):
        if x % 10 == 0:
            print(f"{x}/{xmax}")
        # top row, moving down
        beam = Beam((x, ymin), Direction.DOWN)
        results.append(trace_beam(matrix, beam))
        # bottom row, moving up
        beam = Beam((x, ymax), Direction.UP)
        results.append(trace_beam(matrix, beam))
    print("doing vertical beams...")
    for y in range(ymin, ymax + 1):
        if y % 10 == 0:
            print(f"{y}/{ymax}")
        # left col, moving right
        beam = Beam((y, xmin), Direction.RIGHT)
        results.append(trace_beam(matrix, beam))
        # right col, moving left
        beam = Beam((y, xmax), Direction.LEFT)
        results.append(trace_beam(matrix, beam))
    return max(results)


def trace_beam(matrix: SparseMatrix, start: Beam = Beam((0, 0), Direction.RIGHT)):
    # all the squares visited by the beam will be stored here
    energised = set[Coord]()

    history = set[Beam]()
    active_beams = set[Beam]()
    active_beams.add(start)
    while active_beams:
        history |= active_beams
        new_beams = set[Beam]()
        for beam in active_beams:
            energised.add(beam.coord)
            new_beams |= iterate_beam(beam, matrix)
        active_beams = new_beams
        active_beams -= history  # don't loop infinitely

    return len(energised)


def iterate_beam(beam: Beam, matrix: SparseMatrix) -> set[Beam]:
    """
    1. handle any collisions (which may turn the beam but not move it)
    2. move beam(s) forward
    3. return the new beam(s)

    handle
    - beam hits empty space
    - beam hits mirror
    - beam hits splitter
    - beam exits grid (dies)

    empty return value means all beams died
    """
    # 1
    current_value = matrix[beam.coord]
    beams = set[Beam]()
    if current_value in SPLITTERS:
        beams |= collide_splitter(beam, current_value)
    elif current_value in MIRRORS:
        beams |= collide_mirror(beam, current_value)
    else:  # empty square; beam continues
        beams = {beam}
    # 2
    new_beams = set[Beam]()
    for beam in beams:
        next_coord = get_next_square(beam)
        if next_coord not in matrix:
            continue  # beam dies
        beam = Beam(next_coord, beam.direction)
        new_beams.add(beam)
    return new_beams


def collide_splitter(beam: Beam, splitter: str) -> set[Beam]:
    if beam.direction in {Direction.RIGHT, Direction.LEFT}:
        if splitter == "|":
            #    ^      ^
            # >>>|  or  |<<<
            #    v      v
            return {
                Beam(beam.coord, Direction.DOWN),
                Beam(beam.coord, Direction.UP),
            }
        if splitter == "-":
            # >>>->>>
            #    or
            # <<<-<<<
            return {beam}  # beam passes thru
    elif beam.direction in {Direction.UP, Direction.DOWN}:
        if splitter == "|":
            # v      ^
            # v      ^
            # |  or  |
            # v      ^
            # v      ^
            return {beam}
        if splitter == "-":
            #  v
            # <->  or  <->
            #           ^
            return {
                Beam(beam.coord, Direction.LEFT),
                Beam(beam.coord, Direction.RIGHT),
            }


def collide_mirror(beam: Beam, mirror: str) -> set[Beam]:
    """
    A mirror cannot split beams, so we can just return the direction
    """
    direction = beam.direction
    new_direction: Direction
    if mirror == "/":
        if direction == Direction.RIGHT:
            #   ^
            # >>/
            new_direction = Direction.UP
        elif direction == Direction.LEFT:
            # \<<
            # v
            new_direction = Direction.DOWN
        elif direction == Direction.UP:
            # />>
            # ^
            new_direction = Direction.RIGHT
        else:
            #  v
            # </
            new_direction = Direction.LEFT
    else:  # mirror = \
        if direction == Direction.RIGHT:
            # >\
            #  v
            new_direction = Direction.DOWN
        elif direction == Direction.LEFT:
            # ^
            # \<
            new_direction = Direction.UP
        elif direction == Direction.UP:
            # <\
            #  ^
            new_direction = Direction.LEFT
        else:
            # v
            # \>
            new_direction = Direction.RIGHT
    return {Beam(beam.coord, new_direction)}


def parse_input(input: str) -> SparseMatrix:
    return SparseMatrix.from_str(input)


def get_next_square(beam: Beam) -> Coord:
    x, y = beam.coord
    return {
        Direction.RIGHT: (x + 1, y),
        Direction.LEFT: (x - 1, y),
        Direction.DOWN: (x, y + 1),
        Direction.UP: (x, y - 1),
    }[beam.direction]
