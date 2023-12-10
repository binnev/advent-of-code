import re

from typing import Callable

import utils

Nodes = dict[str, tuple[str, str]]
State = tuple[int, str]  # iteration_number, node_id


@utils.profile
def part1(input: str):
    instructions, nodes = parse_input(input)
    instructions_len = len(instructions)
    ii = 0
    node_id = "AAA"
    while True:
        if node_id == "ZZZ":
            break
        instruction = instructions[ii % instructions_len]
        node_id = do_iteration(node_id, instruction, nodes)
        ii += 1
    return ii


@utils.profile
def part2(input: str):
    instructions, nodes = parse_input(input)
    instructions_len = len(instructions)
    ii = 0
    node_ids = [id for id in nodes if id.endswith("A")]
    while True:
        if all(id.endswith("Z") for id in node_ids):
            break

        instruction = instructions[ii % instructions_len]
        node_ids = [do_iteration(node_id, instruction, nodes) for node_id in node_ids]

        ii += 1
    return ii


def simulate_trajectory(node_id: str, instructions: str, nodes: Nodes) -> list[State]:
    wrap = len(instructions)
    ii = 0
    output = []
    while True:
        output.append((ii, node_id))  # 1 add value
        if node_id.endswith("Z"):
            break
        instruction = instructions[ii % wrap]  # iterate
        node_id = do_iteration(node_id, instruction, nodes)
        ii += 1  # update ii
    return output


def calculate_endpoints(
    node_id: str, n_endpoints: int, instructions: str, nodes: Nodes
) -> list[int]:
    """
    Find out on which iterations we land on an endpoint
    By calculating based on the loop length
    """
    intro, loop = find_cycle(node_id, instructions, nodes)

    # for each endpoint we encountered, find the iteration on which we first landed on it.
    endpoint_iterations = []
    for ii, (_, node_id) in enumerate(loop):
        if node_id.endswith("Z"):
            endpoint_iterations.append(ii + len(intro))

    result = []
    n = 0
    while len(result) < n_endpoints:
        for endpoint_ii in endpoint_iterations:
            if len(result) >= n_endpoints:
                break
            result.append(endpoint_ii + len(loop) * n)
        n += 1
    return result


def get_endpoint_checker(node_id: str, instructions: str, nodes: Nodes) -> Callable[[int], bool]:
    """
    Generate a function that, for a given trajectory, checks if an iteration number is an endpoint.
    """
    intro, loop = find_cycle(node_id, instructions, nodes)
    intro_len = len(intro)
    loop_len = len(loop)

    endpoint_iterations = []
    for ii, (_, node_id) in enumerate(loop):
        if node_id.endswith("Z"):
            endpoint_iterations.append(ii + intro_len)

    def checker(iteration: int) -> bool:
        for endpoint_ii in endpoint_iterations:
            if iteration == endpoint_ii:
                return True
            elif iteration > endpoint_ii:
                if (iteration - endpoint_ii) % loop_len == 0:
                    return True
            else:
                pass  # ignore ii smaller than the known endpoints
        return False

    return checker


def simulate_endpoints2(
    node_id: str, n_endpoints: int, instructions: str, nodes: Nodes
) -> list[int]:
    results = []
    ii = 0
    checker = get_endpoint_checker(node_id, instructions, nodes)
    while True:
        if checker(ii):
            results.append(ii)
        if len(results) >= n_endpoints:
            break
        ii += 1
    return results


def simulate_endpoints(
    node_id: str, n_endpoints: int, instructions: str, nodes: Nodes
) -> list[int]:
    """
    Find out on which iterations we land on an endpoint
    By simulating every iteration
    """
    wrap = len(instructions)
    ii = 0
    endpoints = []
    while True:
        if node_id.endswith("Z"):
            endpoints.append(ii)
        if len(endpoints) == n_endpoints:
            break

        instruction = instructions[ii % wrap]  # iterate
        node_id = do_iteration(node_id, instruction, nodes)
        ii += 1  # update ii
    return endpoints


def find_cycle(node_id: str, instructions: str, nodes: Nodes) -> tuple[list[State], list[State]]:
    length = len(instructions)
    ii = 0
    # Store state history. State is a combination of instruction index and node_id
    history = []

    while True:
        # prepare the state
        # - which node are we at
        # - which where are we on the instructions loop?
        instruction_index = ii % length
        instruction = instructions[instruction_index]
        state = (instruction_index, node_id)

        # add state to history (or break)
        if state in history:
            break
        history.append(state)

        # update veriables for the next iteration
        node_id = do_iteration(node_id, instruction, nodes)
        ii += 1

    loop_start = history.index(state)
    intro = history[:loop_start]
    loop = history[loop_start:]
    return intro, loop


def do_iteration(node_id: str, instruction: str, nodes: Nodes) -> str:
    left_id, right_id = nodes[node_id]
    if instruction == "L":
        node_id = left_id
    else:
        node_id = right_id
    return node_id


def parse_input(input: str) -> tuple[str, dict[str, tuple[str, str]]]:
    lines = input.splitlines()
    instructions = lines[0]
    nodes = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        id, left, right = match.groups()
        nodes[id] = (left, right)

    return instructions, nodes


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day8")
    part2(input)
