import re
from typing import NamedTuple

from python import utils

example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ResourceDict = dict[str, int]  # e.g. {ORE: 3, CLAY: 4, ...}
BluePrint = dict[str, ResourceDict]


def parse_input(input: str) -> dict[int, BluePrint]:
    blueprints = dict()
    for line in input.splitlines():
        number = int(re.search("Blueprint (\d+):", line).groups()[0])
        blueprint = BluePrint()
        blueprints[number] = blueprint
        robot_costs = line.split(": ")[1].split(". ")
        for cost in robot_costs:
            robot_type = re.search("Each (\w+) robot", cost).groups()[0]
            blueprint[robot_type] = ResourceDict()
            rest = cost.split("robot costs ")[1]
            foo = re.findall("(\d+) (\w+)", rest)
            for amount, resource in foo:
                blueprint[robot_type][resource] = int(amount)
    return blueprints


def have_resources(required: ResourceDict, resources: ResourceDict) -> bool:
    return all(resources[resource] >= amount for resource, amount in required.items())


def start_building_robot(robot_type: str, required: ResourceDict, resources: ResourceDict):
    # start building robot
    print(f"Spend {required.items()} to start building a " f"{robot_type}-collecting robot.")

    # remove spent resources immediately
    for resource, amount in required.items():
        resources[resource] -= amount


def make_plan(blueprint: BluePrint) -> list[str]:
    """
    Work out in what order to build robots to maximise geode production.
    We want to build as many geode robots as possible; for that we need the resources,
    and for that we need other robots...

    Time is also a factor; building a Clay robot first will net us rolling clay income.
    """
    example_blueprint = {
        "ore": {"ore": 4},
        "clay": {"ore": 2},
        "obsidian": {"ore": 3, "clay": 14},
        "geode": {"ore": 2, "obsidian": 7},
    }
    # to be able to regularly build geode robots, we need to get our ore:obsidian flux to 2:7.
    # what do we need for that?
    # 2 ore robots and 7 obsidian robots.
    """
                               ORE     CLAY        OBSI
    geode       
    - ore flux 2                   
        - ore robots 2
            - ore 4 each 
    - obsidian 7    
        - obsidian robots 7    
            - ore 3 each                
            - clay 14 each         
                - 
    """
    # todo: work this out programmatically *gulp*
    robot_build_queue = [CLAY, CLAY, CLAY, CLAY, OBSIDIAN, OBSIDIAN, GEODE, GEODE]
    # robot_build_queue = [CLAY, CLAY, CLAY, OBSIDIAN, CLAY, OBSIDIAN, GEODE, GEODE]
    return robot_build_queue


def execute_plan(build_queue: list[str], blueprint: BluePrint) -> int:
    income: ResourceDict = {ORE: 1}  # you start with 1 ore-collecting robot
    resources: ResourceDict = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    next_robot_to_build = build_queue.pop(0)
    required_resources = blueprint[next_robot_to_build]
    for ii in range(24):
        print("")
        print(f"== Minute {ii + 1} ==")

        # build robots
        building_robot = False
        if next_robot_to_build:
            if have_resources(required_resources, resources):
                # start building robot
                building_robot = True
                spent = ", ".join(
                    f"{amount} {resource}" for resource, amount in required_resources.items()
                )
                print(
                    f"Spend {spent} to start building a " f"{next_robot_to_build}-collecting robot."
                )

                # remove spent resources immediately
                for resource, amount in required_resources.items():
                    resources[resource] -= amount

        # collect income
        for material, flux in income.items():
            resources[material] += flux
            print(
                f"{flux} {material}-collecting robot collects {flux} {material}; "
                f"you now have {resources[material]} {material}"
            )

        # add any new robots
        if building_robot:
            income[next_robot_to_build] = income.get(next_robot_to_build, 0) + 1
            print(
                f"The new {next_robot_to_build}-collecting robot is ready; "
                f"you now have {income[next_robot_to_build]} of them."
            )
            if build_queue:
                next_robot_to_build = build_queue.pop(0)
                required_resources = blueprint[next_robot_to_build]

    return resources[GEODE]


def handle_blueprint(blueprint: BluePrint) -> int:
    robot_build_queue = make_plan(blueprint)
    geodes = execute_plan(robot_build_queue, blueprint)
    return geodes


def improvise(blueprint: BluePrint) -> int:
    """
    Instead of a predetermined build queue, how about a tech tree of priorities? Ultimately we
    want geode-producing robots. But what do we need in order to get THEM? And what requirements
    do THOSE robots have?

    RULES:
    - If you can build a geode miner, do it now (seems obvious)
    -
    """

    income: ResourceDict = {ORE: 1}  # you start with 1 ore-collecting robot
    resources: ResourceDict = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    for ii in range(24):
        print("")
        print(f"== Minute {ii + 1} ==")

        # build robots
        robot_type = None
        for material in [GEODE, OBSIDIAN, CLAY, ORE]:
            # Don't build so many of a machine that you get more resources than you can use per
            # minute. The max resources we can use per minute is the blueprint with the max of
            # that resource
            max_consumption = max(costs.get(material, 0) for robot_type, costs in blueprint.items())
            if material == GEODE:
                max_consumption = 9999
            need_more = income.get(material, 0) < max_consumption
            if have_resources(required=blueprint[material], resources=resources) and need_more:
                robot_type = material
                spent = ", ".join(
                    f"{amount} {resource}" for resource, amount in blueprint[material].items()
                )
                print(f"Spend {spent} to start building a " f"{robot_type}-collecting robot.")

                # remove spent resources immediately
                for resource, amount in blueprint[material].items():
                    resources[resource] -= amount

        # collect income
        for material, flux in income.items():
            resources[material] += flux
            print(
                f"{flux} {material}-collecting robot collects {flux} {material}; "
                f"you now have {resources[material]} {material}."
            )

        # add any new robots
        if robot_type:
            income[robot_type] = income.get(robot_type, 0) + 1
            print(
                f"The new {robot_type}-collecting robot is ready; "
                f"you now have {income[robot_type]} of them."
            )

    return resources[GEODE]


def calculate_max_geodes(blueprint: BluePrint, minutes: int) -> int:
    limits = {
        material: max(costs.get(material, 0) for robot_type, costs in blueprint.items())
        for material in [ORE, CLAY, OBSIDIAN]
    }
    limits[GEODE] = 999999

    class State(NamedTuple):
        description: str
        # you start with 1 ore-collecting robot
        income: ResourceDict = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
        resources: ResourceDict = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}

    current = State(description="initial state")
    frontier = [current]
    for minute in range(minutes):
        frontier = sorted(frontier, key=lambda x: x.resources[GEODE], reverse=True)[:10000]
        # print(f"===== minute {minute} =====")
        # print(f"{len(frontier)=}")
        max_geodes = max(state.resources[GEODE] for state in frontier)
        max_obs = max(state.resources[OBSIDIAN] for state in frontier)
        # print(f"{max_geodes=}")
        # print(f"{max_obs=}")
        neighbours = []
        for state in frontier:
            # building new robots
            for material in [GEODE, OBSIDIAN, CLAY, ORE]:
                need_more = state.income[material] < limits[material]
                previous_resources = {
                    mat: amount - state.income[mat] for mat, amount in state.resources.items()
                }
                recipe = blueprint[material]
                coulda = have_resources(
                    required=recipe,
                    resources=previous_resources,
                )
                if (
                    have_resources(
                        required=recipe,
                        resources=state.resources,
                    )
                    and need_more
                    and not coulda
                ):
                    new_state = State(
                        description=f"Build {material} robot",
                        income=state.income.copy(),
                        resources=state.resources.copy(),
                    )
                    # pay for the robot
                    for resource, amount in recipe.items():
                        new_state.resources[resource] -= amount
                    # collect income
                    for resource, amount in new_state.income.items():
                        new_state.resources[resource] += amount
                    # increase income thanks to new robot
                    new_state.income[material] += 1
                    neighbours.append(new_state)
            # waiting and collecting income
            new_state = State(
                description=f"Wait...",
                income=state.income.copy(),
                resources=state.resources.copy(),
            )
            for resource, amount in new_state.income.items():
                new_state.resources[resource] += amount
            neighbours.append(new_state)

        frontier = neighbours
    max_geodes = max(state.resources[GEODE] for state in frontier)
    return max_geodes


@utils.profile
def part1():
    """
    Which blueprint maximises the number of opened geodes after 24 minutes?
    """
    # input = example
    input = utils.load_puzzle_input("2022/day19")
    blueprints = parse_input(input)
    result = 0
    for id, blueprint in blueprints.items():
        max_geodes = calculate_max_geodes(blueprint, 24)
        print(f"blueprint {id} generates {max_geodes=}")
        result += max_geodes * id
    return result


@utils.profile
def part2():
    # input = example
    input = utils.load_puzzle_input("2022/day19")
    blueprints = parse_input(input)
    result = 1
    for id, blueprint in blueprints.items():
        if id > 3:
            break
        max_geodes = calculate_max_geodes(blueprint, 32)
        print(f"blueprint {id} generates {max_geodes=}")
        result *= max_geodes
    return result


if __name__ == "__main__":
    assert part1() == 1766
    assert part2() == 30780
