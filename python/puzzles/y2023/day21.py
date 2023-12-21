"""
NOTES:

It appears to be impossible to completely fill an area with Os. They always alternate on/off.

So what I could do is see if the number of steps is even or odd, and then just bfs outwards from
the start, and mark each even (or odd) step with Os.

Next step after that: don't set the Os along the way; bfs out and calculate how many squares will
be covered. Then calculate how many of them will be Os

Can I predict whether a square will be O or . based purely on its coordinates?

"""


import utils
from utils import SparseMatrix, Coord

WALL = "#"
REACHABLE = "░"


@utils.profile
def part1(input: str):
    matrix, start = parse_input(input)
    reachable = forgetful_bfs({start}, matrix, 64)
    return len(reachable)


@utils.profile
def part2(input: str):
    pass


def hopeful_maths(frontier: set[Coord], matrix: SparseMatrix, steps: int) -> int:
    """
    1. With no walls, the number of activated squares after N steps is (N+1)**2

    2. We know where the walls are, we just need to check if they block an active
    square. A wall blocks an active square if is_odd(taxicab_distance(S, wall)) == is_odd(N)

    3. The number of active squares after N steps is 1. - 2.
    """
    start = list(frontier)[0]
    ideally_reachable_squares = (steps + 1) ** 2
    walls = {coord: value for coord, value in matrix.items() if value == WALL}
    walls_that_block = {}
    for coord, value in walls.items():
        dist = taxicab_dist(start, coord)
        oddness_matches = is_odd(dist) == is_odd(steps)
        inside_diamond = taxicab_dist(coord, start) <= steps
        if oddness_matches and inside_diamond:
            walls_that_block[coord] = value
    return ideally_reachable_squares - len(walls_that_block)


def is_odd(n: int) -> bool:
    return n % 2 != 0


def bfs_once(frontier: set[Coord], matrix: SparseMatrix, steps: int) -> int:
    even_steps = steps % 2 == 0
    marked = 0
    if even_steps:
        marked += len(frontier)
    visited = frontier
    for ii in range(1, steps + 1):
        new_frontier = set()
        for node in frontier:
            new_frontier |= get_neighbours(node, matrix)
        new_frontier -= visited

        frontier = new_frontier

        even_ii = ii % 2 == 0
        if (even_steps and even_ii) or (not even_steps and not even_ii):
            marked += len(frontier)

    return marked


def forgetful_bfs_summary(frontier: set[Coord], matrix: SparseMatrix, steps: int) -> int:
    return len(forgetful_bfs(frontier, matrix, steps))


def forgetful_bfs(frontier: set[Coord], matrix: SparseMatrix, steps: int) -> set[Coord]:
    """
    This will be just like bfs except we don't maintain a "visited" set, and we can revisit squares.
    """
    for _ in range(steps):
        new_frontier = set()
        for node in frontier:
            new_frontier |= get_neighbours(node, matrix)
        frontier = new_frontier
    return frontier


def get_neighbours(coord: Coord, matrix: SparseMatrix) -> set[Coord]:
    x, y = coord
    potential = {
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    }
    return {c for c in potential if c in matrix and matrix[c] == "."}


def parse_input(input: str) -> tuple[SparseMatrix, Coord]:
    matrix = SparseMatrix.from_str(input.strip())
    # matrix = SparseMatrix(
    #     {coord: (WALL if value == "#" else value) for coord, value in matrix.items()}
    # )
    start = next(coord for coord, value in matrix.items() if value == "S")
    matrix[start] = "."
    return matrix, start


def taxicab_dist(a: Coord, b: Coord) -> int:
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day21")
    print(input)
