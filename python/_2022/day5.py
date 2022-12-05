from python import utils

raw = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse_input():
    input = utils.load_puzzle_input("2022/day5")
    # parse state
    state_str, instructions_str = input.split("\n\n")
    state_lines = state_str.split("\n")
    number_row = state_lines[-1]
    num_cols = len(number_row.split())
    state_lines = [l.ljust(len(number_row)) for l in state_lines]
    state = {n + 1: [] for n in range(num_cols)}
    for row in state_lines[-2::-1]:
        for col in range(num_cols):
            x = 1 + col * 4
            if row[x].strip():
                state[col + 1].append(row[x])

    # parse instructions
    instructions = [
        list(
            map(
                int,
                line.replace("move ", "").replace(" from", "").replace(" to", "").strip().split(),
            )
        )
        for line in instructions_str.split("\n")
    ]
    return state, instructions


def move(origin: int, destination: int, state: dict):
    state[destination].append(state[origin].pop())


def move9001(amount: int, origin: int, destination: int, state: dict):
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
        move9001(amount, origin, destination, state)
    return "".join(state[key][-1] for key in sorted(state.keys()))


if __name__ == "__main__":
    assert part1() == "GRTSWNJHH"
    assert part2() == "QLFQDBBHM"
