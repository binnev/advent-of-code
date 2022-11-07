import time
from collections import deque, Counter

from _2021.python import utils

raw = utils.load_puzzle_input("day14")


def init():
    polymer, substitutions = raw.split("\n\n")
    substitutions = [line.split(" -> ") for line in substitutions.splitlines()]
    substitutions = {pair: char for pair, char in substitutions}
    return polymer, substitutions


def get_pairs(string):
    return [string[ii : ii + 2] for ii in range(len(string) - 1)]


def expand(polymer, substitutions):
    """This expands the string by depth 1. This is the fastest thing I could find for part 1."""
    right = deque(polymer)
    ll = right.popleft()
    left = deque(ll)
    for rr in right:
        if middle := substitutions.get(ll + rr):
            left.append(middle)
        left.append(rr)
        ll = rr
    return "".join(left)


def galaxy_brain(polymer, substitutions, depth):
    """
    Don't worry about the order! Instead, count the *pairs* of characters, and expand them. For
    each expansion, add the middle character to the total counts. Don't need to store the whole
    string, and can do bulk operations for all the occurrances of each pair!
    """
    totals = Counter(polymer)
    pairs = Counter(get_pairs(polymer))
    for ii in range(depth):
        new_pairs = Counter()
        for pair, count in pairs.items():
            if middle := substitutions.get(pair, ""):
                totals[middle] += count
                new_pairs += {pair[0] + middle: count, middle + pair[-1]: count}
            else:
                # if this pair isn't in substitutions, it didn't increment the counter. And it
                # won't next time either, so no point including it in new_pairs
                pass
        pairs = new_pairs

    most_common = totals.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


@utils.profile
def part1():
    """Brute force; actually calculating the whole expanded string"""
    polymer, substitutions = init()
    for ii in range(10):
        polymer = expand(polymer, substitutions)
    totals = Counter(polymer)
    most_common = totals.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


@utils.profile
def part2():
    polymer, substitutions = init()
    return galaxy_brain(polymer, substitutions, depth=40)


if __name__ == "__main__":
    assert part1() == 2590
    assert part2() == 2875665202438
