from python import utils
import numpy as np

example = """30373
25512
65332
33549
35390"""


def parse_input(input: str) -> np.ndarray:
    return np.array([list(map(int, line)) for line in input.split("\n")])


def is_visible_in_row(x: int, row: np.ndarray) -> bool:
    height = row[x]
    left = row[:x]
    right = row[x + 1 :]
    if not len(left) or not len(right):
        return True  # edges always visible
    result = height > left.max() or height > right.max()
    return result


def is_visible_from_edge(x: int, y: int, grid: np.ndarray) -> bool:
    row = grid[y, :]
    col = grid[:, x]
    return is_visible_in_row(x, row) or is_visible_in_row(y, col)


def scenic_score_row(x: int, row: list[int]) -> int:
    height = row[x]
    left = row[:x]
    right = row[x + 1 :]
    lscore = rscore = 0
    for tree in reversed(left):
        lscore += 1
        if tree >= height:
            break
    for tree in right:
        rscore += 1
        if tree >= height:
            break
    return lscore * rscore


def scenic_score(x: int, y: int, grid: np.ndarray) -> int:
    row = grid[y, :]
    col = grid[:, x]
    xscore = scenic_score_row(x, list(row))
    yscore = scenic_score_row(y, list(col))
    return xscore * yscore


@utils.profile
def part1() -> int:
    input = utils.load_puzzle_input("2022/day8")
    grid = parse_input(input)
    count = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if is_visible_from_edge(x=x, y=y, grid=grid):
                count += 1
    return count


@utils.profile
def part2() -> int:
    input = utils.load_puzzle_input("2022/day8")
    grid = parse_input(input)
    max_score = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            score = scenic_score(x=x, y=y, grid=grid)
            if score > max_score:
                max_score = score
    return max_score


if __name__ == "__main__":
    assert part1() == 1698
    assert part2() == 672280
