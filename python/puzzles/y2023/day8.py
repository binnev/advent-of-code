import re
import utils


Node = tuple[str, str, str]


@utils.profile
def part1(input: str):
    instructions, nodes = _parse_input(input)
    instructions_len = len(instructions)
    ii = 0
    node_id = "AAA"
    while True:
        if node_id == "ZZZ":
            break
        left_id, right_id = nodes[node_id]
        instruction = instructions[ii % instructions_len]
        if instruction == "L":
            node_id = left_id
        else:
            node_id = right_id

        ii += 1
    return ii


@utils.profile
def part2(input: str):
    ...


def _parse_input(input: str) -> tuple[str, dict[str, tuple[str, str]]]:
    lines = input.splitlines()
    instructions = lines[0]
    nodes = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", line)
        id, left, right = match.groups()
        nodes[id] = (left, right)

    return instructions, nodes


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day8")
    part1(input)
