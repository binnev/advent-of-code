from python import utils
import re

example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse_input():
    input = utils.load_puzzle_input("2022/day5")
    state_str, instructions_str = input.split("\n\n")

    # parse state
    state_lines = state_str.split("\n")
    num_cols = len(state_lines[-1].split())
    state = {n + 1: [] for n in range(num_cols)}
    for row in state_lines[-2::-1]:
        for col in range(num_cols):
            x = 1 + col * 4
            try:
                if row[x].strip():
                    state[col + 1].append(row[x])
            except IndexError:  # final column doesn't reach this high
                pass

    # parse instructions
    rx = re.compile("move (\d+) from (\d+) to (\d+)")
    instructions = [list(map(int, rx.search(l).groups())) for l in instructions_str.split("\n")]
    return state, instructions


def move(origin: int, destination: int, state: dict, amount: int = 1):
    state[origin], crates = state[origin][:-amount], state[origin][-amount:]
    state[destination].extend(crates)


@utils.profile
def part1() -> str:
    state, instructions = parse_input()
    for amount, origin, destination in instructions:
        for _ in range(amount):
            move(origin, destination, state)
    return "".join(state[key][-1] for key in sorted(state.keys()))


@utils.profile
def part2() -> str:
    state, instructions = parse_input()
    for amount, origin, destination in instructions:
        move(origin, destination, state, amount=amount)
    return "".join(state[key][-1] for key in sorted(state.keys()))


if __name__ == "__main__":
    assert part1() == "GRTSWNJHH"
    assert part2() == "QLFQDBBHM"
