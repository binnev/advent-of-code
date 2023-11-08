import utils
import numpy as np

example = """30373
25512
65332
33549
35390"""


def parse_input(raw: str) -> np.ndarray:
    return np.array([list(map(int, line)) for line in raw.split("\n")])


def is_visible_1d(x: int, row: np.ndarray) -> bool:
    """Is the tree visible in a 1D row of trees"""
    height = row[x]
    left = row[:x]
    right = row[x + 1 :]
    if not len(left) or not len(right):
        return True  # edges always visible
    result = height > left.max() or height > right.max()
    return result


def is_visible_2d(x: int, y: int, grid: np.ndarray) -> bool:
    """Is the tree visible in a 2D grid of trees"""
    row = grid[y, :]
    col = grid[:, x]
    return is_visible_1d(x, row) or is_visible_1d(y, col)


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
def part1(raw: str) -> int:
    grid = parse_input(raw)
    count = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if is_visible_2d(x=x, y=y, grid=grid):
                count += 1
    return count


@utils.profile
def part2(raw: str) -> int:
    grid = parse_input(raw)
    max_score = 0
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            score = scenic_score(x=x, y=y, grid=grid)
            if score > max_score:
                max_score = score
    return max_score


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day8")
    assert part1(raw) == 1698
    assert part2(raw) == 672280
