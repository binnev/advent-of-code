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


class Node:
    id: str
    flow_rate: int
    neighbours: "Nodes"

    def __init__(self, id, flow_rate):
        self.id = id
        self.flow_rate = flow_rate
        self.neighbours = Nodes()

    def link(self, other: "Node"):
        self.neighbours[other.id] = other
        other.neighbours[self.id] = self

    def __repr__(self):
        return (
            f"Node("
            f"id={self.id}, "
            f"flow={self.flow_rate}, "
            f"neighbours={list(self.neighbours.keys())})"
        )


Nodes = dict[str, Node]
Distances = dict[str, int]
DistanceMap = dict[str, Distances]
Adjacency = dict[str, set[str]]
FlowRates = dict[str, int]


class State(NamedTuple):
    description: str
    node: str
    release_rate: int
    open_valves: tuple[str]
    minute: int
    pressure_released: int


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
    nonzero_nodes: set[str],
    dist_map: DistanceMap,
    flow_rates: FlowRates,
) -> list[State]:
    """
    Either open the current valve, or go to another valve (with nonzero flow_rate that hasn't
    already been opened)

    Go to each of the nonzero, non-opened valves and create a new State for that
    """
    unopened = [node for node in nonzero_nodes if node not in current.open_valves]

    # to prevent pointless walking around: if you are standing on an unopened node, always open it.
    if current.node in unopened:
        return [
            State(
                description=f"Open valve {current.node}",
                node=current.node,
                release_rate=current.release_rate + flow_rates[current.node],
                open_valves=(*current.open_valves, current.node),
                minute=current.minute + 1,  # flat 1 minute to open valve
                pressure_released=current.pressure_released + current.release_rate,
            )
        ]
    # if all valves have been opened, just wait
    if not unopened:
        return [
            State(
                description="Waiting...",
                node=current.node,
                release_rate=current.release_rate,
                open_valves=current.open_valves,
                minute=current.minute + 1,  # flat 1 minute to open valve
                pressure_released=current.pressure_released + current.release_rate,
            )
        ]
    # otherwise, create a list of unopened nodes to walk to
    next_states = []
    for node in unopened:
        distance = dist_map[current.node][node]
        time_taken = distance * 1  # 1 minute to walk between nodes
        next_states.append(
            State(
                description=f"Walking to valve {node}",
                node=node,
                release_rate=current.release_rate,
                open_valves=current.open_valves,
                minute=current.minute + time_taken,
                pressure_released=current.pressure_released + current.release_rate * time_taken,
            )
        )
    return next_states


@utils.profile
def part1():
    """
    875 too low
    Traveling Purchaser Problem https://en.wikipedia.org/wiki/Traveling_purchaser_problem

    create graph of State space
    State(
        node: str
        release_rate: int
    )
    """
    # input = example
    input = utils.load_puzzle_input("2022/day16")
    adjacency, flow_rates = parse_input(input)
    dist_map = crunch_distance_map(adjacency)
    nonzero_nodes = {node for node, flow in flow_rates.items() if flow > 0}

    # bfs through the state space

    start = State(
        description="initial state",
        node="AA",
        release_rate=0,
        pressure_released=0,
        open_valves=tuple(),
        minute=0,
    )
    frontier = {start}
    max_pressure_released = 0
    ii = 0
    while frontier:
        print(f"===== Iteration {ii} =====")
        print(f"{len(frontier)=}")

        finished = {state for state in frontier if state.minute == 30}
        print(f"{len(finished)} finished runs")
        for f in finished:
            # print(f"\tFinished state: {f}")
            f: State
            if f.pressure_released > max_pressure_released:
                print(f"\t\tNew record for pressure released: {f.pressure_released}, "
                      f"with valve order {', '.join(f.open_valves)}")
                max_pressure_released = f.pressure_released
        frontier = frontier - finished

        timed_out = {state for state in frontier if state.minute > 30}
        print(f"{len(timed_out)} runs exceeded 30 minutes")
        for f in timed_out:
            # print(f"\tTimed-out state: {f}. Back-calculating pressure at 30 minutes...")
            overtime = f.minute - 30
            back_pressure = f.pressure_released - f.release_rate * overtime
            # print(f"\t\tAt 30 minutes, the pressure released was {back_pressure}")
            if back_pressure > max_pressure_released:
                print(f"\t\tNew record for pressure released: {back_pressure}, "
                      f"with valve order {', '.join(f.open_valves)}")
                max_pressure_released = back_pressure
        frontier = frontier - timed_out

        # prune the frontier to consider only the 100 best runs
        frontier = sorted(
            frontier, key=lambda x: x.pressure_released / (x.minute or 1), reverse=True
        )[:12000]

        # fixme: this isn't working. Step through the nodes one at a time and add a "visited" dict
        #  where the key is (node, release_rate), and the value is (pressure_released, minute).
        #  This way the frontier only grows proportional to the number of neighbours each node
        #  has (instead of with the total number of nodes, which is way more).
        options = set()
        for state in frontier:
            state_options = get_next_states(
                current=state,
                nonzero_nodes=nonzero_nodes,
                dist_map=dist_map,
                flow_rates=flow_rates,
            )
            options = options.union(state_options)

        frontier = options
        ii += 1
    return max_pressure_released


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
