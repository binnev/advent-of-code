import utils
import re

example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


Columns = dict[int, str]
Instructions = list[list[int]]


def parse_input(input: str) -> tuple[Columns, Instructions]:
    state_str, instructions_str = input.split("\n\n")

    # parse state: flip columns to rows and grab the rows that contain the actual data; ignore
    # rows containing brackets etc.
    state_lines = [line.ljust(40) for line in state_str.split("\n")]
    state = {
        int(chars[-1]): "".join(reversed(chars[:-1])).strip()
        for chars in zip(*state_lines)
        if chars[-1].isnumeric()  # the columns end with the column number
    }

    # parse instructions
    rx = re.compile("move (\d+) from (\d+) to (\d+)")
    instructions = [list(map(int, rx.search(l).groups())) for l in instructions_str.split("\n")]
    return state, instructions


def move(origin: int, destination: int, state: dict, amount: int = 1):
    state[origin], crates = state[origin][:-amount], state[origin][-amount:]
    state[destination] += crates


@utils.profile
def part1() -> str:
    input = utils.load_puzzle_input("2022/day5")
    state, instructions = parse_input(input)
    for amount, origin, destination in instructions:
        for _ in range(amount):
            move(origin, destination, state)
    return "".join(state[key][-1] for key in sorted(state.keys()))


@utils.profile
def part2() -> str:
    input = utils.load_puzzle_input("2022/day5")
    state, instructions = parse_input(input)
    for amount, origin, destination in instructions:
        move(origin, destination, state, amount=amount)
    return "".join(state[key][-1] for key in sorted(state.keys()))


if __name__ == "__main__":
    assert part1() == "GRTSWNJHH"
    assert part2() == "QLFQDBBHM"
