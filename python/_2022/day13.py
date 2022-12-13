from python import utils

example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def parse_input(input: str) -> list[tuple[str, str]]:
    output = []
    for packet_pair in input.split("\n\n"):
        left, right = packet_pair.splitlines()
        output.append((left, right))
    return output


def are_integers_ordered(left: int, right: int) -> bool | None:
    if left < right:
        return True
    elif left > right:
        return False
    else:
        return None


def are_lists_ordered(left: list, right: list) -> bool | None:
    for a, b in zip(left, right):
        ordered = are_packets_ordered(a, b)
        if ordered is not None:
            return ordered

    # if we reached the end, one of the lists ran out of items: if the left one is shorter,
    # they're ordered
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False
    else:
        return None  # same order


def are_packets_ordered(left: int | list, right: int | list) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        return are_integers_ordered(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        return are_lists_ordered(left, right)
    elif isinstance(left, int) and isinstance(right, list):
        return are_lists_ordered([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return are_lists_ordered(left, [right])
    else:
        raise Exception(f"Not sure how to parse {left=}, {right=}")


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day13")
    packets = parse_input(input)
    score = 0
    for ii, (left, right) in enumerate(packets):
        left = eval(left)
        right = eval(right)
        ordered = are_packets_ordered(left, right)
        if ordered:
            score += ii + 1
    return score


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    assert part1() == 6420
    part2()
