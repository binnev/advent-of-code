import utils
from utils import SparseMatrix, Coord


@utils.profile
def part1(input: str):
    matrix, start = parse_input(input)
    reachable = forgetful_bfs({start}, matrix, 64)
    return len(reachable)


@utils.profile
def part2(input: str):
    pass


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
    start = next(coord for coord, value in matrix.items() if value == "S")
    matrix[start] = "."
    return matrix, start


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day21")
    part1(input)
