import utils


def init(raw: str):
    coords, folds = raw.split("\n\n")
    matrix = {tuple(map(int, row.split(","))): "#" for row in coords.splitlines()}
    fold_instructions = []
    for fold in folds.splitlines():
        direction, position = fold.split("=")
        direction = direction[-1]
        position = int(position)
        fold_instructions.append((direction, position))
    return matrix, fold_instructions


def print_matrix(matrix: dict):
    xs = [key[0] for key in matrix]
    ys = [key[1] for key in matrix]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(matrix.get((x, y), "."), end="")
        print("")


def fold_up(matrix, fold_y):
    new_matrix = {}
    for x, y in matrix:
        if y > fold_y:
            dist = y - fold_y
            new_y = fold_y - dist
            new_matrix[(x, new_y)] = matrix[(x, y)]
        else:
            new_matrix[(x, y)] = matrix[(x, y)]
    return new_matrix


def fold_left(matrix, fold_x):
    new_matrix = {}
    for x, y in matrix:
        if x > fold_x:
            dist = x - fold_x
            new_x = fold_x - dist
            new_matrix[(new_x, y)] = matrix[(x, y)]
        else:
            new_matrix[(x, y)] = matrix[(x, y)]
    return new_matrix


@utils.profile
def part1(raw: str):
    matrix, fold_instructions = init(raw)
    mapping = {"x": fold_left, "y": fold_up}
    direction, position = fold_instructions[0]
    fold_func = mapping[direction]
    matrix = fold_func(matrix, position)
    return len(matrix)


@utils.profile
def part2(raw: str):
    matrix, fold_instructions = init(raw)
    mapping = {"x": fold_left, "y": fold_up}
    for direction, position in fold_instructions:
        fold_func = mapping[direction]
        matrix = fold_func(matrix, position)
    return len(matrix)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day13")
    assert part1(raw) == 655
    assert part2(raw) == 95
