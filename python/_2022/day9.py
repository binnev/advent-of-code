from python import utils

example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

larger_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


Coord = tuple[int, int]


def sign(x: int) -> int:
    return 1 if x >= 0 else -1


def move_head(head: Coord, direction: str) -> Coord:
    match direction:
        case "R":
            return (head[0] + 1, head[1])
        case "L":
            return (head[0] - 1, head[1])
        case "U":
            return (head[0], head[1] - 1)
        case "D":
            return (head[0], head[1] + 1)


def move_tail(head: Coord, tail: Coord) -> Coord:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    if abs(dx) > 1 or abs(dy) > 1:
        new_x, new_y = tail
        if dy != 0:
            new_y = tail[1] + sign(dy)
        if dx != 0:
            new_x = tail[0] + sign(dx)
        return (new_x, new_y)
    else:  # still touching; do nothing
        return tail


def print_path(tail_history: set[Coord]):
    xs = [x for x, y in tail_history]
    ys = [y for x, y in tail_history]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (x, y) in tail_history else ".", end="")
        print("")


def plot_path(tail_history: set[Coord]):
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import numpy

    xs = numpy.array([x for x, y in tail_history])
    ys = numpy.array([y for x, y in tail_history])

    # shift all coords into positive
    xs = xs - min(xs)
    ys = ys - min(ys)

    # build image
    width = max(xs) + 1
    height = max(ys) + 1
    img = numpy.zeros((width, height))
    for x, y in zip(xs, ys):
        img[x, y] = 1

    fig, ax = plt.subplots()
    ax: Axes
    ax.imshow(img.T)
    plt.show()


@utils.profile
def part1():
    head = (0, 0)
    tail = (0, 0)

    input = utils.load_puzzle_input("2022/day9")
    tail_history = {tail}
    for line in input.split("\n"):
        direction, amount = line.split()
        amount = int(amount)
        for _ in range(amount):
            head = move_head(head, direction)
            tail = move_tail(head, tail)
            tail_history.add(tail)

    return len(tail_history)


@utils.profile
def part2():
    snake = [(0, 0)] * 10
    input = utils.load_puzzle_input("2022/day9")
    tail_history = {snake[-1]}
    for line in input.split("\n"):
        direction, amount = line.split()
        amount = int(amount)
        for _ in range(amount):
            snake[0] = move_head(snake[0], direction)
            for ii, part in enumerate(snake[1:], start=1):
                snake[ii] = move_tail(head=snake[ii - 1], tail=snake[ii])
            tail_history.add(snake[-1])
    return len(tail_history)


if __name__ == "__main__":
    assert part1() == 6494
    assert part2() == 2691
