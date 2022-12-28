import itertools
import math
import re

from typing import NamedTuple

from python import utils

example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


Distances = dict[str, int]
DistanceMap = dict[str, Distances]
Adjacency = dict[str, set[str]]
FlowRates = dict[str, int]


class State(NamedTuple):
    description: str
    node: str
    release_rate: int
    open_valves: tuple[str]
    pressure_released: int

    @property
    def hash(self):
        return (self.node, self.release_rate, self.open_valves)


class State2(NamedTuple):
    description: str
    nodes: tuple[str, str]  # left is you, right is elephant
    release_rate: int
    open_valves: tuple[str]
    pressure_released: int

    @property
    def hash(self):
        return (self.nodes, self.release_rate, self.open_valves)


def parse_input(input: str) -> tuple[Adjacency, FlowRates]:
    rx = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    adjacency = dict()
    flow_rates = dict()
    for line in input.splitlines():
        id, flow_rate, neighbours = rx.search(line).groups()
        flow_rate = int(flow_rate)
        neighbours = set(neighbours.split(", "))
        adjacency[id] = neighbours
        flow_rates[id] = flow_rate
    return adjacency, flow_rates


def get_distances(start_id: str, adjacency: Adjacency) -> Distances:
    visited = set()

    frontier = [start_id]
    distances: Distances = {start_id: 0}
    neighbour_dist = 1
    while True:
        neighbours = set()
        for node in frontier:
            for n in adjacency[node]:
                if n not in visited:
                    neighbours.add(n)

        if not neighbours:
            break  # finished exploring

        for node in neighbours:
            dist = min(distances.get(node, math.inf), neighbour_dist)
            distances[node] = dist

        visited = visited.union(frontier)
        frontier = neighbours
        neighbour_dist += 1

    return distances


def crunch_distance_map(adjacency: Adjacency) -> DistanceMap:
    dist_map = DistanceMap()
    for id in adjacency:
        distances = get_distances(start_id=id, adjacency=adjacency)
        dist_map[id] = distances
    return dist_map


def get_next_states(
    current: State,
    adjacency: Adjacency,
    flow_rates: FlowRates,
    nonzero_nodes: set[str],
) -> list[State]:
    """
    Either open the current valve, or go to another valve (with nonzero flow_rate that hasn't
    already been opened)

    Go to each of the nonzero, non-opened valves and create a new State for that
    """
    unopened = [node for node in nonzero_nodes if node not in current.open_valves]
    # if all options have been exhausted, just wait
    if not unopened:
        return [
            State(
                description=f"Waiting...",
                node=current.node,
                release_rate=current.release_rate,
                open_valves=current.open_valves,
                pressure_released=current.pressure_released + current.release_rate,
            )
        ]
    next_states = []
    if flow_rates[current.node] > 0 and current.node not in current.open_valves:
        next_states.append(
            State(
                description=f"Open node {current.node}",
                node=current.node,
                release_rate=current.release_rate + flow_rates[current.node],
                open_valves=(*current.open_valves, current.node),
                pressure_released=current.pressure_released + current.release_rate,
            )
        )
    for neighbour in adjacency[current.node]:
        next_states.append(
            State(
                description=f"Walk to node {neighbour}",
                node=neighbour,
                release_rate=current.release_rate,
                open_valves=current.open_valves,
                pressure_released=current.pressure_released + current.release_rate,
            )
        )
    return next_states


def get_next_states_with_elephant(
    current: State2,
    adjacency: Adjacency,
    flow_rates: FlowRates,
    nonzero_nodes: set[str],
) -> list[State2]:
    human_state = State(
        description="Temporary human state",
        node=current.nodes[0],
        release_rate=current.release_rate,
        open_valves=current.open_valves,
        pressure_released=current.pressure_released,
    )
    human_options = get_next_states(
        current=human_state,
        adjacency=adjacency,
        flow_rates=flow_rates,
        nonzero_nodes=nonzero_nodes,
    )
    elephant_state = State(
        description="Temporary elephant state",
        node=current.nodes[1],
        release_rate=current.release_rate,
        open_valves=current.open_valves,
        pressure_released=current.pressure_released,
    )
    elephant_options = get_next_states(
        current=elephant_state,
        adjacency=adjacency,
        flow_rates=flow_rates,
        nonzero_nodes=nonzero_nodes,
    )
    new_states = []
    for human_option in human_options:
        for elephant_option in elephant_options:
            open_valves = human_option.open_valves + tuple(
                v for v in elephant_option.open_valves if v not in human_option.open_valves
            )
            release_rate = sum(flow_rates[v] for v in open_valves)
            new_state = State2(
                description=f"Human {human_option.description}; Elephant {elephant_option.description}",
                nodes=(human_option.node, elephant_option.node),
                pressure_released=current.pressure_released + current.release_rate,
                release_rate=release_rate,
                open_valves=open_valves,
            )
            new_states.append(new_state)
    return new_states


@utils.profile
def part1():
    """
    This is still really inefficient.
    """
    input = utils.load_puzzle_input("2022/day16")
    adjacency, flow_rates = parse_input(input)
    nonzero_nodes = {node for node, flow in flow_rates.items() if flow > 0}
    start = State(
        description="Initial state.",
        node="AA",
        release_rate=0,
        open_valves=tuple(),
        pressure_released=0,
    )
    visited = {start.hash: start}
    frontier = {start}
    for minute in range(30):
        options = set()
        for state in frontier:
            for neighbouring_state in get_next_states(
                state,
                adjacency,
                flow_rates,
                nonzero_nodes,
            ):
                if (
                    neighbouring_state.hash not in visited
                    or neighbouring_state.description == "Waiting..."
                ):
                    options.add(neighbouring_state)
            visited[state.hash] = state
        frontier = options

        print(f"===== Minute {minute+1} =====")
        print(f"{len(frontier)=}")
        print("Top runs so far:")
        top10 = sorted(frontier, key=lambda s: s.pressure_released, reverse=True)[:5]
        for top in top10:
            print(f"\t{top}")
    return max(state.pressure_released for state in frontier)


@utils.profile
def part2():
    """
    todo:
    halve the search space by not considering mirror options.
    """
    # input = example
    input = utils.load_puzzle_input("2022/day16")
    adjacency, flow_rates = parse_input(input)
    nonzero_nodes = {node for node, flow in flow_rates.items() if flow > 0}
    start = State2(
        description="Initial state.",
        nodes=("AA", "AA"),
        release_rate=0,
        open_valves=tuple(),
        pressure_released=0,
    )
    visited = {start.hash: start}
    frontier = {start}
    for minute in range(26):
        options = set()
        for state in frontier:
            for neighbouring_state in get_next_states_with_elephant(
                state,
                adjacency,
                flow_rates,
                nonzero_nodes,
            ):
                if (
                    neighbouring_state.hash not in visited
                    or "Waiting..." in neighbouring_state.description
                ):
                    options.add(neighbouring_state)
            visited[state.hash] = state
        frontier = options
        frontier = sorted(frontier, key=lambda s: s.pressure_released, reverse=True)[:100000]
        print(f"===== Minute {minute+1} =====")
        print(f"{len(frontier)=}")
        print("Top runs so far:")
        top10 = frontier[:5]
        for top in top10:
            print(f"\t{top}")
    return max(state.pressure_released for state in frontier)


if __name__ == "__main__":
    assert part1() == 2056
    assert part2() == 2513
