import re

from python import utils
from python._2022.day14 import SparseMatrix, print_sparse_matrix, Coord

example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
ARROWS = {
    RIGHT: ">",
    LEFT: "<",
    UP: "^",
    DOWN: "v",
}
WALL = "#"


def parse_map(map_str: str) -> SparseMatrix:
    grid = SparseMatrix()
    for y, line in enumerate(map_str.splitlines()):
        for x, value in enumerate(line):
            if value.strip():
                grid[(x, y)] = value
    return grid


def parse_instructions(instructions_str: str) -> list[str]:
    rx = re.compile("(\d+|\w)")
    instructions = rx.findall(instructions_str)
    return instructions


def parse_input(input: str) -> (SparseMatrix, ...):
    map_str, instructions_str = input.split("\n\n")
    grid = parse_map(map_str)
    instructions = parse_instructions(instructions_str)
    return grid, instructions


def get_next_square(pos: Coord, facing: int, grid: SparseMatrix) -> Coord:
    current_x, current_y = pos
    mapping = {
        RIGHT: (current_x + 1, current_y),
        LEFT: (current_x - 1, current_y),
        UP: (current_x, current_y - 1),
        DOWN: (current_x, current_y + 1),
    }
    next_square = mapping[facing]
    if next_square not in grid:
        if facing == RIGHT:
            next_x = min(x for x, y in grid if y == current_y)
            next_square = (next_x, current_y)
        if facing == LEFT:
            next_x = max(x for x, y in grid if y == current_y)
            next_square = (next_x, current_y)
        if facing == UP:
            next_y = max(y for x, y in grid if x == current_x)
            next_square = (current_x, next_y)
        if facing == DOWN:
            next_y = min(y for x, y in grid if x == current_x)
            next_square = (current_x, next_y)
    return next_square


def get_next_square_folded(pos: Coord, facing: int, faces: SparseMatrix, edges) -> Coord:
    current_x, current_y = pos
    mapping = {
        RIGHT: (current_x + 1, current_y),
        LEFT: (current_x - 1, current_y),
        UP: (current_x, current_y - 1),
        DOWN: (current_x, current_y + 1),
    }
    next_square = mapping[facing]
    new_facing = facing
    if next_square not in faces:
        current_face = int(faces[pos])
        mapping_, direction_change = edges[(current_face, facing)]
        next_square = mapping_[pos]
        new_facing = facing + direction_change
    return next_square, new_facing


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day22")
    grid, instructions = parse_input(input)
    start_x = min(x for x, y in grid if y == 0)
    pos = (start_x, 0)
    facing = RIGHT
    grid[pos] = ARROWS[facing]

    for instruction in instructions:
        if instruction.isnumeric():
            num_steps = int(instruction)
            for _ in range(num_steps):
                next_square = get_next_square(pos, facing, grid)
                if grid[next_square] == WALL:
                    break
                else:
                    pos = next_square
                grid[pos] = ARROWS[facing]

        else:
            if instruction == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
            grid[pos] = ARROWS[facing]

    row = pos[1] + 1
    col = pos[0] + 1
    return 1000 * row + 4 * col + facing


def gcd(a: int, b: int) -> int:
    """Greatest common divisor"""
    a_factors = utils.prime_factors(a)
    b_factors = utils.prime_factors(b)
    common_factors = set(a_factors.keys()) & set(b_factors.keys())
    common = {factor: min(a_factors[factor], b_factors[factor]) for factor in common_factors}
    result = 1
    for factor, exponent in common.items():
        result *= factor**exponent
    return result


def get_cube_face_size(grid: SparseMatrix) -> int:
    """I know I could just hard-code this..."""
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return gcd(height, width)


def get_coloured_grid(grid: SparseMatrix, face_size: int) -> SparseMatrix:
    coloured = SparseMatrix()
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    num_x = width // face_size
    num_y = height // face_size
    ii = 0
    for yy in range(num_y):
        for xx in range(num_x):
            face_xs = range(xx * face_size, xx * face_size + face_size)
            face_ys = range(yy * face_size, yy * face_size + face_size)
            placed = all((x, y) in grid for x in face_xs for y in face_ys)
            if placed:
                for x in face_xs:
                    for y in face_ys:
                        coloured[(x, y)] = str(ii + 1)
                ii += 1
    return coloured


def get_left_edge(face_id: int, coloured: SparseMatrix):
    """
    Relying very much on the ordering of dict keys here. It's guaranteed not to be random,
    but it does depend on the order I inserted the entries. Given that I worked top-to-bottom in
    the input string, and never change the `coloured` grid after creating it, I think it's safe.

    | +----+
    | |    |
    | |    |
    V +----+
    """
    face = {(x, y): val for (x, y), val in coloured.items() if val == str(face_id)}
    edge_x = min(x for x, y in face)
    return [(x, y) for (x, y) in face if x == edge_x]


def get_right_edge(face_id: int, coloured: SparseMatrix):
    """
    +----+ |
    |    | |
    |    | |
    +----+ V
    """
    face = {(x, y): val for (x, y), val in coloured.items() if val == str(face_id)}
    edge_x = max(x for x, y in face)
    return [(x, y) for (x, y) in face if x == edge_x]


def get_top_edge(face_id: int, coloured: SparseMatrix):
    """
    ----->
    +----+
    |    |
    |    |
    +----+
    """
    face = {(x, y): val for (x, y), val in coloured.items() if val == str(face_id)}
    edge_y = min(y for x, y in face)
    return [(x, y) for (x, y) in face if y == edge_y]


def get_bottom_edge(face_id: int, coloured: SparseMatrix):
    """
    +----+
    |    |
    |    |
    +----+
    ----->
    """

    face = {(x, y): val for (x, y), val in coloured.items() if val == str(face_id)}
    edge_y = max(y for x, y in face)
    return [(x, y) for (x, y) in face if y == edge_y]


@utils.profile
def part2():
    # input = utils.load_puzzle_input("2022/day22")
    input = example
    grid, instructions = parse_input(input)
    instructions = parse_instructions("LL2")
    coloured = get_coloured_grid(grid, face_size=get_cube_face_size(grid))
    start_x = min(x for x, y in grid if y == 0)
    pos = (start_x, 0)
    facing = RIGHT
    grid[pos] = ARROWS[facing]

    print_sparse_matrix(grid, empty_char=" ")
    print_sparse_matrix(coloured, empty_char=" ")

    # we need something for when we step off the edge of a tile. Depending on the tile we were
    # on, we need to do a certain transform.
    RELATIONS = {
        (1, LEFT): (
            {a: b for a, b in zip(get_left_edge(1, coloured), get_top_edge(3, coloured))},
            -1,
        ),
        (3, UP): (
            {a: b for a, b in zip(get_top_edge(3, coloured), get_left_edge(1, coloured))},
            1,
        ),
    }

    for instruction in instructions:
        if instruction.isnumeric():
            num_steps = int(instruction)
            for _ in range(num_steps):
                next_square, new_facing = get_next_square_folded(
                    pos, facing, faces=coloured, edges=RELATIONS
                )
                if grid[next_square] == WALL:
                    break
                else:
                    facing = new_facing
                    pos = next_square
                grid[pos] = ARROWS[facing]
                print_sparse_matrix(grid, empty_char=" ")

        else:
            if instruction == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
            grid[pos] = ARROWS[facing]
            print_sparse_matrix(grid, empty_char=" ")

    # print_sparse_matrix(grid, empty_char=" ")
    row = pos[1] + 1
    col = pos[0] + 1
    return 1000 * row + 4 * col + facing


if __name__ == "__main__":
    assert part1() == 65368
    # part2()
