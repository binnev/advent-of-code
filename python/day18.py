import re
from collections import deque
from itertools import combinations
from math import floor, ceil

raw = """[[[3,[8,6]],[6,1]],[[[1,1],2],[[1,0],0]]]
[[[1,[7,3]],1],9]
[[[2,6],[[3,1],[0,9]]],[[7,[4,8]],[[2,7],3]]]
[[[3,[0,4]],[[8,4],[1,9]]],[7,[2,[5,7]]]]
[[[4,5],[[0,7],1]],[9,[0,4]]]
[[5,[[1,5],[3,6]]],8]
[[3,[[9,3],9]],9]
[2,[[[2,1],[0,5]],[9,9]]]
[[2,[6,9]],[[[4,1],0],[3,4]]]
[[[[6,8],0],[[8,8],9]],[[[4,2],3],[3,[7,3]]]]
[[3,7],9]
[[[[2,5],8],[2,5]],[[0,[5,7]],[[2,5],4]]]
[[[8,[6,6]],0],[4,[[5,6],[8,4]]]]
[[[1,[8,2]],[[0,4],[2,6]]],[[3,4],0]]
[[1,[[9,2],[6,0]]],[[[0,9],5],[[8,0],[1,5]]]]
[[2,[[2,3],[1,8]]],[3,[[7,2],[0,7]]]]
[[5,4],5]
[[[[4,2],[4,8]],[7,3]],[0,[[8,9],6]]]
[[[6,7],0],5]
[[2,[[9,0],[8,4]]],[[[7,4],[3,4]],0]]
[[[9,[8,9]],1],[[5,[6,7]],3]]
[[2,[0,0]],[3,[[2,5],[1,4]]]]
[[0,1],[0,[[8,8],[8,3]]]]
[[[0,2],[2,8]],[1,[[7,0],0]]]
[[[[5,4],3],[[7,5],[2,6]]],[[5,8],[0,1]]]
[0,[0,0]]
[[5,[[5,6],0]],[[[2,7],9],[7,9]]]
[[[[0,8],2],[[2,5],[7,6]]],[[9,7],[[8,7],[9,2]]]]
[[[0,[4,6]],[[6,3],[4,4]]],[8,[[4,8],[4,8]]]]
[[[[8,9],[3,8]],8],[[[7,9],6],[9,[2,7]]]]
[[[[8,9],[1,6]],0],[[[8,7],4],[9,[1,4]]]]
[5,7]
[[[[1,5],[3,6]],[[5,5],4]],[[3,3],[4,[4,0]]]]
[[[0,6],[5,[5,3]]],[[4,[0,0]],8]]
[7,[6,8]]
[[[[8,5],9],[[3,2],7]],[[[6,6],5],2]]
[[[[4,4],[0,4]],9],0]
[[0,[3,[9,3]]],[9,[[8,0],[0,9]]]]
[[[[4,0],0],[1,[1,7]]],[[3,[3,0]],[[1,3],6]]]
[[9,4],[3,[[7,1],6]]]
[[[[3,7],7],1],[[4,3],[[6,9],[6,9]]]]
[[[8,[2,5]],[[8,4],4]],[[[3,4],[6,7]],[5,[8,5]]]]
[2,[4,[[3,2],7]]]
[[[[3,1],[5,6]],[[2,7],7]],[4,[8,[7,4]]]]
[[7,8],[[[3,9],7],2]]
[[[[8,8],[5,8]],[[1,0],[6,0]]],[[[1,2],6],[[4,2],[5,5]]]]
[[1,[0,9]],[[[2,1],1],1]]
[[6,[8,1]],[4,[[7,8],5]]]
[[[1,[1,6]],[1,[5,7]]],[[[2,8],6],0]]
[9,1]
[[[0,[6,5]],[[8,5],2]],[[[2,4],[7,3]],[[1,5],[9,2]]]]
[[[2,7],[0,[3,6]]],[[[1,0],[9,6]],[1,[0,4]]]]
[6,[[[5,9],8],[0,2]]]
[7,[[[9,4],[8,6]],[[1,1],1]]]
[[[2,1],0],8]
[1,[[6,[1,4]],[[0,0],[1,9]]]]
[[[1,[7,9]],2],8]
[[[[0,9],2],[[8,4],9]],[0,[[7,7],[4,8]]]]
[[1,[2,[1,8]]],[[[3,6],[2,1]],[3,[5,0]]]]
[[3,3],[3,5]]
[[[[9,3],[4,3]],[5,[8,1]]],[[6,[5,0]],9]]
[0,[[9,[3,5]],3]]
[[[9,1],0],[[[5,9],[8,0]],[7,[4,8]]]]
[[[[7,7],8],3],[[[6,6],[6,5]],[6,4]]]
[[[[3,7],1],[9,[4,2]]],[[9,[2,5]],[[9,0],5]]]
[5,[[0,2],6]]
[[[[2,7],[5,3]],[1,8]],2]
[[[8,[7,7]],[9,[0,0]]],4]
[[[4,[1,4]],0],[[[8,7],8],[[4,1],7]]]
[[[[0,6],0],[[3,2],[9,8]]],[[9,[4,5]],[[7,7],[0,8]]]]
[[[[6,3],3],[[1,5],7]],[[0,1],[7,7]]]
[[[[2,0],2],[3,[3,5]]],[[[0,8],[8,2]],[[0,6],5]]]
[[[6,[5,3]],[[5,5],9]],[[5,9],[[8,7],[3,7]]]]
[[[[1,7],[3,4]],[9,2]],1]
[[[[8,2],6],1],[[5,[2,7]],[3,9]]]
[5,[5,7]]
[[[[9,8],[3,4]],[[2,5],[5,6]]],[[[2,7],7],[9,[8,7]]]]
[[[1,4],[[6,1],[1,3]]],[1,[7,[1,7]]]]
[[[[1,4],8],[[5,1],8]],[[[1,3],[6,9]],[6,[3,3]]]]
[[[[4,0],[0,7]],[4,5]],[4,2]]
[3,8]
[7,[[[7,6],5],[[6,6],5]]]
[[[5,[0,5]],[4,4]],[3,[[4,2],[7,0]]]]
[[[[7,9],8],[9,6]],[5,0]]
[[[[3,0],[5,2]],1],[[[6,9],[5,3]],[[2,5],[6,3]]]]
[7,[[[7,7],[4,5]],[9,2]]]
[[7,[[4,2],[9,3]]],[7,[6,1]]]
[7,9]
[[[8,[8,1]],[[7,3],1]],[[9,8],[2,[8,3]]]]
[[[9,3],3],3]
[[[8,[5,7]],[[2,1],[1,3]]],[[[3,5],2],0]]
[[[8,8],0],[[1,4],[[8,6],9]]]
[[9,[3,[3,0]]],[1,7]]
[1,[[[8,8],1],[2,[0,5]]]]
[[0,[1,5]],[9,[0,[9,0]]]]
[1,[[[1,1],[8,3]],[1,8]]]
[[5,[[7,7],[3,3]]],[[[6,6],[7,8]],[1,[0,0]]]]
[[[[6,7],1],[0,2]],[[[4,2],[7,6]],[[8,4],[4,9]]]]
[[6,[[3,3],[9,0]]],[1,[[4,5],4]]]
[[[[3,4],7],[9,0]],[[[4,5],1],[[5,1],[9,3]]]]"""

example = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

# raw = example


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
        changed = False
        string, changed = explode(string)
        if changed:
            continue

        string, changed = split(string)  # easiest place to start
        if changed:
            continue

        if not changed:
            break
    return string


def find_splits(string):
    for match in re.finditer("\d{2,}", string):
        return match.span(), match.group()
    return (0, 0), ""


def split(string):
    (ii, jj), group = find_splits(string)
    if not group:
        return string, False
    new_value = f"[{floor(int(group) / 2)},{ceil(int(group) / 2)}]"
    return substitute(string, ii, jj, new_value), True


def search_left(string):
    rx = re.compile("(\d+)")
    matches = rx.findall(string)
    if not matches:
        return 0, 0, False
    closest = matches[-1]
    ii = string.rindex(closest)
    jj = ii + len(closest)
    number = string[ii:jj]
    return ii, jj, number


def search_right(string):
    rx = re.compile("(\d+)")
    matches = rx.findall(string)
    if not matches:
        return 0, 0, False
    closest = matches[0]
    ii = string.index(closest)
    jj = ii + len(closest)
    number = string[ii:jj]
    return ii, jj, number


def find_explosions(string):
    found = False
    depth = 0
    indices = []
    group = ""
    for ii, char in enumerate(string):
        if char == "[":
            depth += 1

        if depth > 4:
            found = True
            group += char
            indices.append(ii)

        else:
            if found:  # if we already detected a group
                break

        if char == "]":
            depth -= 1

    if not found:
        return string, "", ""
    left = string[: min(indices)]
    right = string[max(indices) + 1 :]

    return left, group, right


def explode(string) -> (str, bool):
    left, group, right = find_explosions(string)
    if not group:
        return string, False

    d1, d2 = group.split(",")
    d1 = "".join(filter(str.isdigit, d1))
    d2 = "".join(filter(str.isdigit, d2))

    aa, bb, left_digit = search_left(left)
    if left_digit:
        new = str(int(left_digit) + int(d1))
        left = substitute(left, aa, bb, new)

    aa, bb, right_digit = search_right(right)
    if right_digit:
        new = str(int(right_digit) + int(d2))
        right = substitute(right, aa, bb, new)

    return left + "0" + right, True


def substitute(string: str, ii, jj, insertion: str) -> str:
    """Used for split"""
    left = string[:ii]
    right = string[jj:]
    return left + insertion + right


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


def part1():
    lines = init()
    string = lines.pop(0)
    for line in lines:
        string = add(string, line)
    result = magnitude(string)
    return result


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
    explode_tests()
    split_tests()
    add_tests()
    magnitude_tests()
    p1 = part1()
    print(f"{p1=}")
    assert p1 == 4243
    p2 = part2()
    print(f"{p2=}")
    assert p2 == 4701
