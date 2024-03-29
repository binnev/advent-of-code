import utils

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


def parse_monkeys(raw: str) -> (dict[str, int], dict[str, tuple]):
    known = dict()
    unknown = dict()
    for line in raw.splitlines():
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
def part1(raw: str):
    # input = example
    known, unknown = parse_monkeys(raw)
    grind_monkeys(unknown, known)
    return known["root"]


@utils.profile
def part2(raw: str):
    """
    Calculate what we can, and then step down the path of unknowns until we reach "humn",
    updating the target number as we go.
    """
    # input = example
    known, unknown = parse_monkeys(raw)
    known.pop("humn")
    # crunch the known side of the tree
    try:
        grind_monkeys(unknown, known)
    except StopIteration:
        pass

    # figure out which side of the root equation we need to follow
    left, op, right = unknown["root"]
    if left in known:
        target_number = known[left]
        current = right
    else:
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
    raw = utils.load_puzzle_input("2022/day21")
    assert part1(raw) == 142707821472432
    assert part2(raw) == 3587647562851
