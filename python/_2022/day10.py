from pprint import pprint
from typing import Callable

from python import utils

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


@utils.profile
def part1():

    input = utils.load_puzzle_input("2022/day10")
    code = input.split("\n")
    tasks = []
    x = 1
    cycle = 0
    signal_strength = 0
    while code or tasks:
        cycle += 1
        if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strength += cycle * x
        if tasks:
            _, amount = tasks.pop()
            x += amount
        else:
            line = code.pop(0)
            match line.split():
                case ["noop"]:
                    pass
                case ["addx", amount]:
                    tasks.append(["addx", int(amount)])
    return signal_strength


def print_sprite(x):
    sprite_str = ["."] * 41
    try:
        sprite_str[x] = sprite_str[x - 1] = sprite_str[x + 1] = "#"
    except IndexError:
        print(x)
    sprite_str = "".join(sprite_str)
    print(f"Sprite position: {sprite_str}")


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day10")
    # input = larger_example
    code = input.split("\n")
    tasks = []
    x = 1
    current_row = 0
    print_sprite(x)
    print("")
    crt_row = []
    crt_rows = []
    for cycle in range(1, 241):
        do_tasks = bool(tasks)
        if not do_tasks:
            line = code.pop(0)
            match line.split():
                case ["noop"]:
                    pass
                case ["addx", amount]:
                    print(f"Start cycle {cycle:>3}: begin executing addx {amount}")
                    tasks.append(["addx", int(amount)])

        row, h = divmod(cycle - 1, 40)
        print(f"During cycle {cycle:>2}: CRT draws pixel in position {h}")
        # h is the horizontal position of the current pixel being drawn
        if h in [x - 1, x, x + 1]:
            pixel = "#"
        else:
            pixel = " "
        if row > current_row:
            current_row = row
            crt_rows.append(crt_row)
            crt_row = []
        else:
            pass
        crt_row.append(pixel)
        print(f"Current CRT row: {''.join(crt_row)}")

        if do_tasks:
            _, amount = tasks.pop()
            x += amount
            print(
                f"End of cycle {cycle:>2}: finish executing addx {amount} (Register X is now {x})"
            )
            print_sprite(x)

        print("")

    crt_rows.append(crt_row)
    return r"\n".join("".join(row) for row in crt_rows)


if __name__ == "__main__":
    assert part1() == 13440
    assert part2() == (
        "###  ###  ####  ##  ###   ##  ####  ##  \\n"
        "#  # #  #    # #  # #  # #  #    # #  # \\n"
        "#  # ###    #  #    #  # #  #   #  #  # \\n"
        "###  #  #  #   # ## ###  ####  #   #### \\n"
        "#    #  # #    #  # # #  #  # #    #  # \\n"
        "#    ###  ####  ### #  # #  # #### #  # "
    )
