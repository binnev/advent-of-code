import re
from itertools import combinations
from math import floor, ceil

from python import utils

raw = utils.load_puzzle_input("2021/day18")


def init():
    return raw.splitlines()


def add(left, right):
    string = f"[{left},{right}]"
    return reducio(string)


def reducio(string):
    """
    To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish number:

    If any pair is nested inside four pairs, the leftmost such pair explodes.
        need to detect depth somehow
    If any regular number is 10 or greater, the leftmost such regular number splits.
    """
    while True:
        string, changed = explode(string)
        if changed:
            continue

        string, changed = split(string)
        if changed:
            continue

        break
    return string


def split(string):
    for match in re.finditer("\d{2,}", string):
        ii, jj = match.span()
        group = match.group()
        new_value = f"[{floor(int(group) / 2)},{ceil(int(group) / 2)}]"
        return substitute(string, ii, jj, new_value), True
    return string, False


def find_explosions(string):
    depth = 0
    right = string
    left = ""
    group = ""
    while True:
        char = right[:1]
        right = right[1:]
        if char == "[":
            depth += 1
        if depth > 4:
            group += char
            if char == "]":
                return left, group, right
        else:
            left += char
        if char == "]":
            depth -= 1
        if left == string:
            return string, "", ""


def explode(string) -> (str, bool):
    left, group, right = find_explosions(string)
    if not group:
        return string, False

    rx = re.compile("\d+")
    d1, d2 = re.findall(rx, group)

    for match in reversed(list(rx.finditer(left))):
        new = str(int(match.group()) + int(d1))
        left = substitute(left, *match.span(), new)
        break

    for match in rx.finditer(right):
        new = str(int(match.group()) + int(d2))
        right = substitute(right, *match.span(), new)
        break

    return left + "0" + right, True


def substitute(string: str, ii, jj, insertion: str) -> str:
    return string[:ii] + insertion + string[jj:]


def magnitude(number):
    if isinstance(number, str):
        number = eval(number)
    if isinstance(number, list):
        return magnitude(number[0]) * 3 + magnitude(number[1]) * 2
    else:
        return number


def explode_tests():
    for string, expected in [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"),
        ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]"),
    ]:
        result, changed = explode(string)
        assert result == expected


def split_tests():
    for string, expected in [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
    ]:
        result, changed = split(string)
        assert result == expected


def add_tests():
    for left, right, expected in [
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        ),
    ]:
        result = add(left, right)
        assert result == expected


def magnitude_tests():
    for string, expected in [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]:
        result = magnitude(string)
        assert result == expected


@utils.profile
def part1():
    lines = init()
    string = lines.pop(0)
    for line in lines:
        string = add(string, line)
    result = magnitude(string)
    return result


@utils.profile
def part2():
    numbers = init()
    combos = list(combinations(numbers, 2))
    highest = 0
    for a, b in combos:
        mag = magnitude(add(a, b))
        highest = max(highest, mag)
        mag = magnitude(add(b, a))
        highest = max(highest, mag)
    return highest


if __name__ == "__main__":
    assert part1() == 4243
    assert part2() == 4701
