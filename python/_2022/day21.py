import operator
from pprint import pprint

from python import utils

example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


rx_number_shouter = "(\w+): (\d+)"
rx_calculator = "(\w+): (\w+) [\*/-\+] (\w+)"


def parse_monkeys(input: str) -> (dict[str, int], dict[str, tuple]):
    known = dict()
    unknown = dict()
    for line in input.splitlines():
        match line.split():
            case [id, left, op, right]:
                id = id.replace(":", "")
                unknown[id] = (left, op, right)
            case [id, number]:
                id = id.replace(":", "")
                known[id] = int(number)
    return known, unknown


def grind_monkeys(unknown: dict[str, tuple], known: dict[str, int]):
    while unknown:
        ids = set(unknown.keys())
        calculated = set()
        for id, (left, op, right) in unknown.items():
            if left in known and right in known:
                mapping = {
                    "-": lambda a, b: a - b,
                    "+": lambda a, b: a + b,
                    "*": lambda a, b: a * b,
                    "/": lambda a, b: a // b,
                }
                func = mapping[op]
                known[id] = func(known[left], known[right])
                calculated.add(id)
        for id in calculated:
            unknown.pop(id)
        if set(unknown.keys()) == ids:
            raise StopIteration("No progress")


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day21")
    known, unknown = parse_monkeys(input)
    grind_monkeys(unknown, known)
    return known["root"]


@utils.profile
def part2():
    """
    Can calculate the side of the tree that "humn" is not involved in. Then we know what value
    we're aiming for.

    Then calculate our side of the tree, but pass down the value we're aiming for through all the
    functions, and divide/mult etc it; eventually when it reaches "humn" it will be the required
    value.

    Now the trick is to figure out which side of the tree we are on...
    """
    # input = example
    input = utils.load_puzzle_input("2022/day21")
    known, unknown = parse_monkeys(input)
    known.pop("humn")
    # crunch the known side of the tree
    try:
        grind_monkeys(unknown, known)
    except StopIteration:
        pass

    left, op, right = unknown["root"]
    if left in known:
        target_number = known[left]
        current = right
    if right in known:
        target_number = known[right]
        current = left

    while True:
        left, op, right = unknown[current]
        if left in known:
            mapping = {
                "/": lambda target, left: left // target,  # was target = left / right
                "*": lambda target, left: target // left,  # was target = left * right
                "+": lambda target, left: target - left,  # was target = left + right
                "-": lambda target, left: left - target,  # was target = left - right
            }
            func = mapping[op]
            left_value = known[left]
            target_number = func(target_number, left_value)
            current = right
        if right in known:
            mapping = {
                "/": lambda target, right: target * right,  # was target = left / right
                "*": lambda target, right: target // right,  # was target = left * right
                "+": lambda target, right: target - right,  # was target = left + right
                "-": lambda target, right: target + right,  # was target = left - right
            }
            func = mapping[op]
            right_value = known[right]
            target_number = func(target_number, right_value)
            current = left
        if current == "humn":
            return target_number


if __name__ == "__main__":
    assert part1() == 142707821472432
    assert part2() == 3587647562851
