from python import utils
from python.utils import SparseMatrix, sparse_matrix_string

example = """noop
addx 3
addx -5"""

larger_example = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def iterate_beam(tasks: list[int], code: list[str]) -> int:
    amount = 0
    if tasks:
        amount = tasks.pop()
    else:
        line = code.pop(0)
        match line.split():
            case ["addx", amount_string]:
                tasks.append(int(amount_string))
    return amount

@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day10")
    code = input.split("\n")
    tasks = list[int]()
    x = 1
    signal_strength = 0
    for cycle in range(1, 221):
        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strength += cycle * x
        x += iterate_beam(tasks, code)
    return signal_strength


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day10")
    code = input.split("\n")
    tasks = list[int]()
    x = 1
    screen = SparseMatrix()
    for cycle in range(0, 240):
        row, pixel_x = divmod(cycle, 40)
        pixel = "#" if x - 1 <= pixel_x <= x + 1 else " "
        screen[(pixel_x, row)] = pixel
        x += iterate_beam(tasks, code)
    return screen.to_str()


if __name__ == "__main__":
    assert part1() == 13440
    assert part2() == (
        "###  ###  ####  ##  ###   ##  ####  ##  \n"
        "#  # #  #    # #  # #  # #  #    # #  # \n"
        "#  # ###    #  #    #  # #  #   #  #  # \n"
        "###  #  #  #   # ## ###  ####  #   #### \n"
        "#    #  # #    #  # # #  #  # #    #  # \n"
        "#    ###  ####  ### #  # #  # #### #  # "
    )
