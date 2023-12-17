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
    scores = dfs(
        matrix=matrix,
        path=[start],
        score=0,
        finish=finish,
    )
    return min(scores)


@utils.profile
def part2(input: str) -> int:
    pass


def dfs(
    matrix: SparseMatrix,
    path: Path,
    score: int,  # the score of this path so far
    finish: Coord,
    direction_history: tuple[Direction, Direction, Direction] = (None, None, None),  # max 3 len
    best_score: int = None,  # lowest known score of a path that reached the finish
) -> list[int]:
    """
    path = the list of coords we've explored so far

    todo:
        - counting distance -- maybe instead of returning paths we can return total heat loss?
    """
    node = path[-1]
    scores = []
    for direction, coord in get_neighbours(node, matrix):
        new_score = score + matrix[coord]
        # Big assumption: the path never needs to cross itself, so we don't allow it.
        # Mainly to prevent infinite loops, but it also excludes solutions with just 1 loop...
        if coord in path:
            continue
        # Paths that go straight for more than 3 iterations are not allowed
        if len(direction_history) == 3 and all(d == direction for d in direction_history):
            continue
        # If the path's score exceeds another known "low score", stop following this path
        if best_score is not None and new_score > best_score:
            continue

        # base case
        if coord == finish:
            scores.append(new_score)
            # every time we reach the finish, update the best score
            if best_score is None:
                best_score = new_score
            else:
                best_score = min(best_score, new_score)
            continue

        # recursive case
        new_scores = dfs(
            matrix=matrix,
            path=path + [coord],
            score=new_score,
            finish=finish,
            direction_history=(*direction_history[1:], direction),
            best_score=best_score,
        )
        scores.extend(new_scores)
        if scores:
            best_score = min(scores)  # is it too little, too late?

    return scores


def get_neighbours(coord: Coord, matrix: SparseMatrix) -> list[tuple[Direction, Coord]]:
    x, y = coord
    possible = {
        Direction.RIGHT: (x + 1, y),
        Direction.DOWN: (x, y + 1),
        Direction.LEFT: (x - 1, y),
        Direction.UP: (x, y - 1),
    }
    return [(dirn, coord) for dirn, coord in possible.items() if coord in matrix]


def parse_input(input: str) -> SparseMatrix[Coord, int]:
    matrix = SparseMatrix.from_str(input)
    return SparseMatrix({coord: int(value) for coord, value in matrix.items()})


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day17")
    part1(input)
