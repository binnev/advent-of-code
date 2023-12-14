import utils
from utils import SparseMatrix, Coord

ROUND = "O"
SQUARE = "#"
EMPTY = "."


@utils.profile
def part1(input: str):
    matrix = parse_input(input)
    slide_north(matrix)
    score = 0
    new_str = matrix.to_str(flip_y=True)
    for yy, line in enumerate(new_str.splitlines()):
        row_value = yy + 1
        count = line.count(ROUND)
        score += count * row_value
    return score


@utils.profile
def part2(input: str):
    ...


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


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day14")
    part2(input)
