import itertools
import math
import re

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


def parse_input(input: str) -> Nodes:
    rx = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    parsed = []
    for line in input.splitlines():
        id, flow_rate, neighbours = rx.search(line).groups()
        flow_rate = int(flow_rate)
        neighbours = neighbours.split(", ")
        parsed.append((id, flow_rate, neighbours))

    nodes = Nodes()
    for id, flow_rate, _ in parsed:
        nodes[id] = Node(id=id, flow_rate=flow_rate)

    for id, _, neighbours in parsed:
        for n in neighbours:
            nodes[id].link(nodes[n])

    return nodes


def score_nodes(nodes: Nodes, start_id: str) -> dict[str:int]:
    start = nodes[start_id]
    visited = set()
    start = nodes[start_id]
    scores = {start_id: start.flow_rate}
    distances = {start_id: 0}
    frontier = [start]
    neighbour_dist = 1  # it takes 1 sec to get to a neighbour
    valve_open_time = 1
    while True:
        neighbours = set()
        for node in frontier:
            for n in node.neighbours.values():
                if n not in visited:
                    neighbours.add(n)

        if not neighbours:
            break  # finished exploring

        for n in neighbours:
            dist = min(distances.get(n.id, math.inf), neighbour_dist)
            distances[n.id] = dist
            score = n.flow_rate / (dist or 1)
            scores[n.id] = score

        visited = visited.union(frontier)
        frontier = neighbours
        neighbour_dist += 1

    return scores


def get_distances(start_id: str, nodes: Nodes) -> Distances:
    visited = set()

    start = nodes[start_id]
    frontier = [start]
    distances: Distances = {start_id: 0}
    neighbour_dist = 1
    while True:
        neighbours = set()
        for node in frontier:
            for n in node.neighbours.values():
                if n not in visited:
                    neighbours.add(n)

        if not neighbours:
            break  # finished exploring

        for n in neighbours:
            dist = min(distances.get(n, math.inf), neighbour_dist)
            distances[n.id] = dist

        visited = visited.union(frontier)
        frontier = neighbours
        neighbour_dist += 1

    return distances


def shortest_path(a: Node, b: Node):
    distances = get_distances(a)  # this is cached
    return distances[b]


def execute_plan(
    plan: list[tuple[str, float]],
    nodes: Nodes,
    start_id: str,
    dist_map: DistanceMap,
) -> int:
    current = nodes[start_id]
    pressure_released = 0
    elapsed_time = 1
    release_rate = 0
    opened = []
    target = None
    while elapsed_time <= 30:
        # print("")
        # print(f"== Minute {elapsed_time} == ")
        # print(f"Valves {opened} are open, releasing {release_rate} pressure")
        pressure_released += release_rate

        if not target:
            # select next target
            if plan:
                id = plan.pop(0)
                target = nodes[id]
                dist = dist_map[current.id][target.id]
            else:
                # idle
                dist = 69
                target = None

        if dist == 0:
            current = target
            opened.append(target.id)
            release_rate += target.flow_rate
            # print(f"You open valve {target.id}")
            target = None
        else:
            if target:
                # print(f"You are moving to {target.id}")
                dist -= 1
            else:
                ...
                # print("You are chilling")

        elapsed_time += 1

    return pressure_released


def crunch_distance_map(nodes: Nodes) -> DistanceMap:
    dist_map = DistanceMap()
    for id in nodes:
        distances = get_distances(start_id=id, nodes=nodes)
        dist_map[id] = distances
    return dist_map


@utils.profile
def part1():
    """
    875 too low
    Traveling Purchaser Problem https://en.wikipedia.org/wiki/Traveling_purchaser_problem

    """
    # input = example
    input = utils.load_puzzle_input("2022/day16")
    nodes = parse_input(input)
    dist_map = crunch_distance_map(nodes)
    nonzero_nodes = [node.id for node in nodes.values() if node.flow_rate > 0]
    num_perms = math.factorial(len(nonzero_nodes))
    print(f"{nonzero_nodes=}")
    print(f"There are {num_perms} permutations to try")
    perms = itertools.permutations(nonzero_nodes, len(nonzero_nodes))
    max_result = 0
    for ii, plan in enumerate(perms):
        result = execute_plan(list(plan), nodes, start_id="AA", dist_map=dist_map)
        if result > max_result:
            max_result = result
            print(f"New record! {ii=} {plan=} {result=}")
        if ii % 100000 == 0:
            progress = ii / num_perms * 100
            print(f"Progress: {progress:.5f}%")
    return max_result


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
