import re

from python import utils
from python.utils import SparseMatrix, Coord

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


def parse_input(input: str) -> (SparseMatrix, list[str]):
    map_str, instructions_str = input.split("\n\n")
    grid = parse_map(map_str)
    instructions = parse_instructions(instructions_str)
    return grid, instructions


def get_next_square(pos: Coord, facing: int) -> Coord:
    current_x, current_y = pos
    mapping = {
        RIGHT: (current_x + 1, current_y),
        LEFT: (current_x - 1, current_y),
        UP: (current_x, current_y - 1),
        DOWN: (current_x, current_y + 1),
    }
    return mapping[facing]


def pacman_wrap(pos: Coord, heading: int, grid: SparseMatrix) -> Coord:
    """
    Teleport to the opposite side of the world a la Pacman.
    """
    current_x, current_y = pos
    if heading == RIGHT:
        next_x = min(x for x, y in grid if y == current_y)
        next_square = (next_x, current_y)
    elif heading == LEFT:
        next_x = max(x for x, y in grid if y == current_y)
        next_square = (next_x, current_y)
    elif heading == UP:
        next_y = max(y for x, y in grid if x == current_x)
        next_square = (current_x, next_y)
    elif heading == DOWN:
        next_y = min(y for x, y in grid if x == current_x)
        next_square = (current_x, next_y)
    else:
        raise ValueError(f"Bad direction: {heading}")
    return next_square


def cube_fold_wrap(
    pos: Coord,
    heading: int,
    faces: SparseMatrix,
    edges: dict[tuple[int, int], tuple[int, int, bool]],
) -> (Coord, int):
    """
    Teleport to the adjacent edge as if the net has been folded into a cube.
    """
    current_face = int(faces[pos])
    current_edge = heading  # if you walk off the right edge, you must be heading right; simple!
    dest_face, dest_edge, flip = edges[(current_face, heading)]
    new_heading = (dest_edge + 2) % 4
    current_edge_nodes = get_edge_nodes(face_id=current_face, edge=current_edge, faces=faces)
    dest_edge_nodes = get_edge_nodes(face_id=dest_face, edge=dest_edge, faces=faces)
    if flip:
        dest_edge_nodes = reversed(dest_edge_nodes)

    node_map = {a: b for a, b in zip(current_edge_nodes, dest_edge_nodes)}
    next_square = node_map[pos]
    return next_square, new_heading


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
    """I know I could just hard-code this... but this ain't called Advent of Hard Code"""
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return gcd(height, width)


def get_faces(grid: SparseMatrix, face_size: int) -> SparseMatrix:
    """
    Create a SparseMatrix with each entry representing the face of that square:
            1111
            1111
            1111
            1111
    222233334444
    222233334444
    222233334444
    222233334444
            55556666
            55556666
            55556666
            55556666
    """
    faces = SparseMatrix()
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
                        faces[(x, y)] = str(ii + 1)
                ii += 1
    return faces


def get_edge_nodes(face_id: int, edge: int, faces: SparseMatrix) -> list[Coord]:
    """
    Relying very much on the ordering of dict keys here. It's guaranteed not to be random,
    but it does depend on the order I inserted the entries. Given that I worked top-to-bottom in
    the input string, and never change the `coloured` grid after creating it, I think it's safe.
             UP
           ----->
        |  +----+  |
        |  |    |  |
    LEFT|  |FACE|  | RIGHT
        V  +----+  V
           ----->
            DOWN
    """
    face = {(x, y): val for (x, y), val in faces.items() if val == str(face_id)}
    if edge == LEFT:
        edge_x = min(x for x, y in face)
        edge_nodes = [(x, y) for (x, y) in face if x == edge_x]
    elif edge == RIGHT:
        edge_x = max(x for x, y in face)
        edge_nodes = [(x, y) for (x, y) in face if x == edge_x]
    elif edge == UP:
        edge_y = min(y for x, y in face)
        edge_nodes = [(x, y) for (x, y) in face if y == edge_y]
    elif edge == DOWN:
        edge_y = max(y for x, y in face)
        edge_nodes = [(x, y) for (x, y) in face if y == edge_y]
    else:
        raise ValueError(f"Bad direction: {edge}")
    return edge_nodes


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
                next_square = get_next_square(pos, facing)
                if next_square not in grid:
                    next_square = pacman_wrap(pos, facing, grid)
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


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day22")
    grid, instructions = parse_input(input)
    faces = get_faces(grid, face_size=get_cube_face_size(grid))
    start_x = min(x for x, y in grid if y == 0)
    pos = (start_x, 0)
    facing = RIGHT
    grid[pos] = ARROWS[facing]

    # todo: do this programmatically...
    # we need something for when we step off the edge of a tile. Depending on the tile we were
    # on, we need to do a certain transform.
    EDGES_EXAMPLE = {
        # (origin_face, edge): (destination_face, edge, direction_change, reverse_nodes),
        (1, LEFT): (3, UP, False),
        (3, DOWN): (5, LEFT, True),
        (1, RIGHT): (6, RIGHT, True),
        (3, DOWN): (5, LEFT, True),
        (4, RIGHT): (6, UP, True),
        (5, DOWN): (2, DOWN, True),
        (2, LEFT): (6, DOWN, True),
    }
    EDGES_REAL = {
        (1, LEFT): (4, LEFT, True),
        (1, UP): (6, LEFT, False),
        (2, DOWN): (3, RIGHT, False),
        (2, RIGHT): (5, RIGHT, True),
        (2, UP): (6, DOWN, False),
        (3, LEFT): (4, UP, False),
        (5, DOWN): (6, RIGHT, False),
    }
    # EDGES = EDGES_EXAMPLE
    EDGES = EDGES_REAL
    # add the reverse rules too
    EDGES.update(
        {tuple(destination): (*origin, flip) for origin, (*destination, flip) in EDGES.items()}
    )
    for instruction in instructions:
        if instruction.isnumeric():
            num_steps = int(instruction)
            for _ in range(num_steps):
                next_square = get_next_square(pos, facing)
                if next_square not in grid:
                    next_square, new_facing = cube_fold_wrap(pos, facing, faces=faces, edges=EDGES)
                    if grid[next_square] != WALL:
                        facing = new_facing
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

    # grid.print(empty_char=" ")
    row = pos[1] + 1
    col = pos[0] + 1
    return 1000 * row + 4 * col + facing


if __name__ == "__main__":
    assert part1() == 65368
    assert part2() == 156166
