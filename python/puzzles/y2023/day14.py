from copy import copy

from typing import TypeVar

import utils
from utils import SparseMatrix, Coord

ROUND = "O"
SQUARE = "#"
EMPTY = "."
V = TypeVar("V")


@utils.profile
def part1(input: str):
    matrix = parse_input(input)
    slide_north(matrix)
    return calculate_load(matrix)


@utils.profile
def part2(input: str):
    matrix = initial_matrix = parse_input(input)
    # detect cycle
    history = []
    for ii in range(1000000000):
        matrix = spin_cycle(matrix)
        if matrix in history:
            break
        history.append(matrix)
    history.append(matrix)

    final_index = get_final_index([m.to_str() for m in history], num_cycles=1000000000)
    final_matrix = history[final_index]
    return calculate_load(final_matrix)


def calculate_load(matrix: SparseMatrix) -> int:
    score = 0
    new_str = matrix.to_str(flip_y=True)
    for yy, line in enumerate(new_str.splitlines()):
        row_value = yy + 1
        count = line.count(ROUND)
        score += count * row_value
    return score


def slide_north(matrix: SparseMatrix):
    y_min, y_max = matrix.get_ylim()
    x_min, x_max = matrix.get_xlim()

    # starting at the top-left corner, read right and down to find round rocks that can move.
    # Move them one by one in the order we find them. Hopefully this will guarantee no weirdness
    # (famous last words)
    for yy in range(y_min, y_max + 1):
        for xx in range(x_min, x_max + 1):
            coord = (xx, yy)
            value = matrix.get(coord)
            if value != ROUND:
                continue

            new_coord = move_rock_north(coord, matrix)
            if new_coord == coord:
                continue
            matrix[new_coord] = matrix.pop(coord)
            matrix[coord] = EMPTY  # important


def move_rock_north(coord: Coord, matrix: SparseMatrix) -> Coord:
    if matrix[coord] != ROUND:
        raise ValueError(f"Not round @ {coord}; it's {matrix[coord]}")

    candidate = coord
    while True:
        above = (candidate[0], candidate[1] - 1)
        # `above in matrix` is necessary to check out-of-bounds
        if above in matrix and matrix[above] == EMPTY:
            candidate = above
        else:
            break
    return candidate


def parse_input(input: str) -> SparseMatrix:
    return SparseMatrix.from_str(input)


def rotate_clockwise(matrix: SparseMatrix) -> SparseMatrix:
    stringified = matrix.to_str()
    rotated_str = rotate_string_clockwise(stringified)
    return SparseMatrix.from_str(rotated_str)


def rotate_string_clockwise(s: str) -> str:
    values = []
    for chars in zip(*s.splitlines()):
        value = "".join(reversed(chars))
        values.append(value)
    return "\n".join(values)


def spin_cycle(matrix: SparseMatrix) -> SparseMatrix:
    matrix = copy(matrix)
    # north is facing up
    slide_north(matrix)  # slide north

    matrix = rotate_clockwise(matrix)  # west is now facing up
    slide_north(matrix)  # slide west

    matrix = rotate_clockwise(matrix)  # south is now facing up
    slide_north(matrix)  # slide south

    matrix = rotate_clockwise(matrix)  # east is now facing up
    slide_north(matrix)  # slide east

    matrix = rotate_clockwise(matrix)  # north is now facing up again
    return matrix


def get_loop_length(sequence: list[V]) -> tuple[int, int]:
    seen = set()
    for ii, value in enumerate(sequence):
        if value in seen:
            loop_len = ii - sequence.index(value)
            loop_start = ii - loop_len
            break
        seen.add(value)
    return loop_start, loop_len


def get_final_index(sequence: list, num_cycles: int) -> int:
    items_before_loop, loop_len = get_loop_length(sequence)
    foo = num_cycles - items_before_loop
    remainder = foo % loop_len
    end_state = items_before_loop + remainder - 1
    return end_state


def get_final_value(history: list[V], num_cycles: int) -> V:
    final_index = get_final_index(history, num_cycles)
    return history[final_index]
