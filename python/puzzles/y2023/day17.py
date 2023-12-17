import enum
from typing import Callable

import utils
from utils import Coord, SparseMatrix


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


Path = list[Coord]


@utils.profile
def part1(input: str) -> int:
    matrix = parse_input(input)
    _, xmax = matrix.get_xlim()
    _, ymax = matrix.get_ylim()
    start = (0, 0)
    finish = (xmax, ymax)
    neighbour_generator = get_neighbour_generator(matrix)
    possible_paths = dfs(
        path=[start],
        neighbours_generator=neighbour_generator,
        finish=finish,
    )
    heat_losses = []
    for path in possible_paths:
        heat_loss = sum(matrix[coord] for coord in path)
        heat_losses.append(heat_loss)
    return min(heat_losses)


@utils.profile
def part2(input: str) -> int:
    pass


def dfs(
    path: Path,
    neighbours_generator: Callable[[Coord], list[tuple[Direction, Coord]]],
    finish: Coord,
    direction_history: tuple[Direction, Direction, Direction] = (None, None, None),  # max 3 len
) -> list[Path]:
    """
    path = the list of coords we've explored so far

    todo:
        - counting distance -- maybe instead of returning paths we can return total heat loss?
    """
    node = path[-1]
    new_paths = []
    for direction, coord in neighbours_generator(node):
        # Big assumption: the path never needs to cross itself, so we don't allow it.
        # Mainly to prevent infinite loops, but it also excludes solutions with just 1 loop...
        if coord in path:
            continue
        # Paths that go straight for more than 3 iterations are not allowed
        if len(direction_history) == 3 and all(d == direction for d in direction_history):
            continue

        # base case
        if coord == finish:
            new_paths.append(path + [coord])  # todo: calculate heat loss here?
            continue

        # recursive case
        new_path = dfs(
            path + [coord],
            neighbours_generator,
            finish,
            direction_history=(*direction_history[1:], direction),
        )
        new_paths.extend(new_path)

    return new_paths


def get_neighbour_generator(
    matrix: SparseMatrix,
) -> Callable[[Coord], list[tuple[Direction, Coord]]]:
    """
    Using a closure to capture the matrix seems needlessly complicated here...
    """

    def neighbour_generator(coord: Coord) -> list[tuple[Direction, Coord]]:
        x, y = coord
        possible = {
            Direction.RIGHT: (x + 1, y),
            Direction.DOWN: (x, y + 1),
            Direction.LEFT: (x - 1, y),
            Direction.UP: (x, y - 1),
        }
        return [(dirn, coord) for dirn, coord in possible.items() if coord in matrix]

    return neighbour_generator


def parse_input(input: str) -> SparseMatrix[Coord, int]:
    matrix = SparseMatrix.from_str(input)
    return SparseMatrix({coord: int(value) for coord, value in matrix.items()})


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day17")
    part1(input)
