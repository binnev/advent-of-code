import re
from itertools import combinations
from math import floor, ceil

import utils


def init(raw: str):
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


@utils.profile
def part1(raw: str):
    lines = init(raw)
    string = lines.pop(0)
    for line in lines:
        string = add(string, line)
    result = magnitude(string)
    return result


@utils.profile
def part2(raw: str):
    numbers = init(raw)
    combos = list(combinations(numbers, 2))
    highest = 0
    for a, b in combos:
        mag = magnitude(add(a, b))
        highest = max(highest, mag)
        mag = magnitude(add(b, a))
        highest = max(highest, mag)
    return highest


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day18")
    assert part1(raw) == 4243
    assert part2(raw) == 4701
