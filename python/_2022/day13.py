from dataclasses import dataclass

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


def get_list(string: str, start: int) -> tuple[str, int]:
    depth = 1
    ii = start + 1
    while depth:
        char = string[ii]
        match char:
            case "[":
                depth += 1
            case "]":
                depth -= 1
        ii += 1
    result = string[start:ii]
    return result, ii


def get_number(string: str, start: int) -> tuple[str, int]:
    ii = start
    while ii < len(string):
        char = string[ii]
        if not char.isnumeric():
            break
        ii += 1
    result = string[start:ii]
    return result, ii


def get_values(string: str) -> list[str]:
    string = string[1:-1]  # string always starts / ends with [ / ]
    values = list[str]()
    ii = 0
    while ii < len(string):
        char = string[ii]
        if char.isnumeric():
            value, ii = get_number(string, ii)
            values.append(value)
        elif char == "[":
            value, ii = get_list(string, ii)
            values.append(value)
        else:
            ii += 1
    return values


def are_packets_ordered(left: str, right: str, depth=0) -> bool | None:
    indent = "\t" * depth
    # print(f"{indent}Compare {left} vs {right}")

    # both ints
    if left.isnumeric() and right.isnumeric():
        if int(left) < int(right):
            # print(f"{indent}\tLeft side is smaller, so inputs are in the right order")
            return True
        if int(left) == int(right):
            return None
        else:
            # print(f"{indent}\tRight side is smaller, so inputs are not in the right order")
            return False  # right integer is larger

    # mixed types
    if left.isnumeric() and not right.isnumeric():
        converted = f"[{left}]"
        # print(f"{indent}\tMixed types; convert left to {converted} and retry comparison")
        return are_packets_ordered(converted, right, depth + 1)
    if right.isnumeric() and not left.isnumeric():
        converted = f"[{right}]"
        # print(f"{indent}\tMixed types; convert right to {converted} and retry comparison")
        return are_packets_ordered(left, converted, depth + 1)

    # both list
    left_values = get_values(left)
    right_values = get_values(right)
    left_len = len(left_values)
    right_len = len(right_values)
    left_shorter = None if left_len == right_len else left_len < right_len
    while True:
        try:
            left_value = left_values.pop(0)
            right_value = right_values.pop(0)
        except IndexError:
            if left_shorter is True:
                # print(f"{indent}\tLeft side ran out of items, so inputs are in the right order")
                return left_shorter
            elif left_shorter is None:
                return left_shorter
            else:
                # print(f"{indent}\tRight side ran out of items, so inputs are not in the right order")
                return left_shorter
        result = are_packets_ordered(left_value, right_value, depth + 1)
        if result is None:
            continue
        else:
            return result


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day13")
    packets = parse_input(input)
    score = 0
    for ii, (left, right) in enumerate(packets, start=1):
        ordered = are_packets_ordered(left, right)
        if ordered:
            score += ii
    return score


@dataclass
class Packet:
    contents: str

    def __lt__(self, other: "Packet") -> bool:
        return are_packets_ordered(self.contents, other.contents)


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day13")
    spaces_removed = input.replace("\n\n", "\n")
    spaces_removed += "\n[[2]]\n[[6]]"
    packets = [Packet(packet) for packet in spaces_removed.splitlines()]
    s = [p.contents for p in sorted(packets)]
    loc2 = s.index("[[2]]") + 1
    loc6 = s.index("[[6]]") + 1
    return loc2 * loc6


if __name__ == "__main__":
    assert part1() == 6420
    assert part2() == 22000
