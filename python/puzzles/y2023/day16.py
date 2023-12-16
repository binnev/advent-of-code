import enum

from typing import NamedTuple

import utils
from utils import SparseMatrix, Coord
import enum

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
    return


def trace_beam(matrix: SparseMatrix):
    # all the squares visited by the beam will be stored here
    # could use a set, but I want to store the directions for debugging
    energised = SparseMatrix()
    beam_path = SparseMatrix()
    beam_path.update({k: v for k, v in matrix.items() if v != EMPTY})

    def _update_beam_path(beam: Beam):
        if beam.coord in beam_path:
            value = beam_path[beam.coord]
            if value in r"\/-|":
                return  # don't overwrite mirrors etc
            if value.isnumeric():
                beam_path[beam.coord] = str(int(value) + 1)
            else:
                beam_path[beam.coord] = "2"
        else:
            beam_path[beam.coord] = DIRECTION_STR[beam.direction]

    history = set[Beam]()
    active_beams = set[Beam]()
    active_beams.add(Beam(coord=(0, 0), direction=Direction.RIGHT))
    while active_beams:
        history |= active_beams
        new_beams = set[Beam]()
        for beam in active_beams:
            _update_beam_path(beam)
            energised[beam.coord] = "#"
            new_beams |= iterate_beam(beam, matrix)
        active_beams = new_beams
        active_beams -= history  # don't loop infinitely

    # print("")
    # print("=" * 20)
    # print("after tracing beam, energised squares are:")
    # beam_path.print(empty_char=".")
    # print("=" * 20)
    # print("and here are the energies:")
    # energised.print()

    return len(energised)


def iterate_beam(beam: Beam, matrix: SparseMatrix) -> set[Beam]:
    """
    1. move beam forward
    2. handle any collisions (which may turn the beam but not move it)
    3. return the new beam(s)

    handle
    - beam hits empty space
    - beam hits mirror
    - beam hits splitter
    - beam exits grid (dies)

    empty return value means all beams died
    """
    # 1
    next_coord = get_next_square(beam)
    beam = Beam(next_coord, beam.direction)
    # 2
    next_value = matrix.get(next_coord)
    if next_value is None:
        return set()  # coord not in grid; beam dies
    elif next_value in SPLITTERS:
        return collide_splitter(beam, next_value)
    elif next_value in MIRRORS:
        return collide_mirror(beam, next_value)
    else:  # empty square; beam continues
        return {beam}


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
    matrix = SparseMatrix.from_str(input)
    return matrix


def get_next_square(beam: Beam) -> Coord:
    return get_neighbours(beam.coord)[beam.direction]


def get_neighbours(coord: Coord) -> dict[Direction, Coord]:
    x, y = coord
    return {
        Direction.RIGHT: (x + 1, y),
        Direction.LEFT: (x - 1, y),
        Direction.DOWN: (x, y + 1),
        Direction.UP: (x, y - 1),
    }


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day16")
    part1(input)
