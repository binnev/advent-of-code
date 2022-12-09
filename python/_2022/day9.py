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
            new = (head[0] + 1, head[1])
        case "L":
            new = (head[0] - 1, head[1])
        case "U":
            new = (head[0], head[1] + 1)
        case "D":
            new = (head[0], head[1] - 1)
    return new


def move_tail(head: Coord, tail: Coord) -> Coord:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    if abs(dx) > 1 or abs(dy) > 1:
        new_x, new_y = tail
        if dy != 0:  # same column
            new_y = tail[1] + sign(dy)
        if dx != 0:
            new_x = tail[0] + sign(dx)

        return (new_x, new_y)
    else:
        return tail


@utils.profile
def part1():
    head = (0, 0)
    tail = (0, 0)

    input = utils.load_puzzle_input("2022/day9")  # example
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
    head = (0, 0)
    tail1 = (0, 0)
    tail2 = (0, 0)
    tail3 = (0, 0)
    tail4 = (0, 0)
    tail5 = (0, 0)
    tail6 = (0, 0)
    tail7 = (0, 0)
    tail8 = (0, 0)
    tail9 = (0, 0)

    input = utils.load_puzzle_input("2022/day9")
    tail_history = {tail9}
    for line in input.split("\n"):
        direction, amount = line.split()
        amount = int(amount)
        for _ in range(amount):
            head = move_head(head, direction)
            tail1 = move_tail(head=head, tail=tail1)
            tail2 = move_tail(head=tail1, tail=tail2)
            tail3 = move_tail(head=tail2, tail=tail3)
            tail4 = move_tail(head=tail3, tail=tail4)
            tail5 = move_tail(head=tail4, tail=tail5)
            tail6 = move_tail(head=tail5, tail=tail6)
            tail7 = move_tail(head=tail6, tail=tail7)
            tail8 = move_tail(head=tail7, tail=tail8)
            tail9 = move_tail(head=tail8, tail=tail9)
            tail_history.add(tail9)

    return len(tail_history)


if __name__ == "__main__":
    assert part1() == 6494
    assert part2() == 2691
