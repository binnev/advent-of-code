import re

import utils
from utils import SparseMatrix, Coord

TRENCH = "#"


@utils.profile
def part1(input: str):
    steps = parse_input(input)
    position = (0, 0)
    matrix = SparseMatrix()
    prev_direction = ""
    right_turns = 0
    for direction, distance, _ in steps:
        if direction == prev_direction:
            raise Exception("I wasn't expecting that")

        for d in range(distance):
            matrix[position] = "#"
            position = move1(position, direction)

        if is_right_turn(direction, prev_direction):
            right_turns += 1
        else:
            right_turns -= 1

        prev_direction = direction

    print("")
    print("after digging trench:")
    matrix.print()

    inside_direction = "R" if right_turns > 0 else "L"
    direction, _, _ = steps[0]
    position = move1((0, 0), direction)
    inside_square = get_inside_square(position, direction, inside_direction)
    inside_squares = bfs(matrix, {inside_square})

    matrix.update({node: "I" for node in inside_squares})
    print("")
    print("after filling center:")
    matrix.print()

    return len(matrix)


def bfs(matrix: SparseMatrix, frontier: set[Coord]) -> set[Coord]:
    visited = set()
    while True:
        neighbours = set()
        for node in frontier:
            neighbours |= get_neighbours(node, matrix)
        neighbours -= visited

        visited |= frontier
        if not neighbours:
            break

        frontier = neighbours
    return visited


def get_neighbours(node: Coord, matrix: SparseMatrix) -> set[Coord]:
    x, y = node
    potential_neighbours = {
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    }
    return {node for node in potential_neighbours if matrix.get(node) != "#"}


def get_inside_square(position: Coord, facing: str, inside_direction: str) -> Coord:
    x, y = position
    if facing == "U":
        if inside_direction == "R":
            return (x + 1, y)
        else:
            return (x - 1, y)
    elif facing == "R":
        if inside_direction == "R":
            return (x, y + 1)
        else:
            return (x, y - 1)
    elif facing == "D":
        if inside_direction == "R":
            return (x - 1, y)
        else:
            return (x + 1, y)
    elif facing == "L":
        if inside_direction == "R":
            return (x, y - 1)
        else:
            return (x, y + 1)


def is_right_turn(dirn: str, prev: str) -> str:
    if (
        (prev == "U" and dirn == "R")
        or (prev == "R" and dirn == "D")
        or (prev == "D" and dirn == "L")
        or (prev == "L" and dirn == "U")
    ):
        return True
    else:
        return False


def fill_center(matrix: SparseMatrix):
    xmin, xmax = matrix.get_xlim()
    ymin, ymax = matrix.get_ylim()
    in_center = False  # are we in the ground surrounded by the trench
    in_trench = False  # are we currently on top of the trench
    previous_previous = False  # great name lol
    previous = False
    current = False
    for xx in range(xmin, xmax + 1):
        for yy in range(ymin, ymax + 1):
            coord = (xx, yy)
            current = matrix.get(coord, None) == TRENCH

            # we hit a wall
            if current and not previous:
                in_trench = True
                in_center = not in_center
            # we leave a wall
            if previous and not current:
                in_trench = False
                # if we were in the wall for just 1 iteration, it means we switched from the
                # center to the outside, or vice versa
                if not previous_previous:
                    in_center = not in_center
                # if we were in the wall for more than 1 iteration, it means we're going along
                # the wall, and we will not actually switch sides

            should_fill = in_center and not in_trench

            if should_fill:
                matrix[coord] = TRENCH

            previous_previous = previous
            previous = current


def move1(position: Coord, direction: str) -> Coord:
    if direction == "R":
        return (position[0] + 1, position[1])
    if direction == "L":
        return (position[0] - 1, position[1])
    if direction == "U":
        return (position[0], position[1] - 1)
    if direction == "D":
        return (position[0], position[1] + 1)


@utils.profile
def part2(input: str):
    pass


def parse_input(input: str) -> list[tuple[str, int, str]]:
    rx = re.compile(r"(R|L|U|D) (\d+) (.*)")
    result = []
    for line in input.splitlines():
        match = rx.match(line)
        if not match:
            raise Exception(f"Couldn't match line: {line}")
        direction, distance, color = match.groups()
        result.append((direction, int(distance), color))
    return result


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day18")
    part1(input)
