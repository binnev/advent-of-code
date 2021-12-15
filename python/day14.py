import math
import time
from collections import deque, Counter
from functools import reduce

raw = """OHFNNCKCVOBHSSHONBNF

SV -> O
KP -> H
FP -> B
VP -> V
KN -> S
KS -> O
SB -> K
BS -> K
OF -> O
ON -> S
VS -> F
CK -> C
FB -> K
CH -> K
HS -> H
PO -> F
NP -> N
FH -> C
FO -> O
FF -> C
CO -> K
NB -> V
PP -> S
BB -> N
HH -> B
KK -> H
OP -> K
OS -> V
KV -> F
VH -> F
OB -> S
CN -> H
SF -> K
SN -> P
NF -> H
HB -> V
VC -> S
PS -> P
NK -> B
CV -> P
BC -> S
NH -> K
FN -> P
SH -> F
FK -> P
CS -> O
VV -> H
OC -> F
CC -> N
HK -> N
FS -> P
VF -> B
SS -> V
PV -> V
BF -> V
OV -> C
HO -> F
NC -> F
BN -> F
HC -> N
KO -> P
KH -> F
BV -> S
SK -> F
SC -> F
VN -> V
VB -> V
BH -> O
CP -> K
PK -> K
PB -> K
FV -> S
HN -> K
PH -> B
VK -> B
PC -> H
BO -> H
SP -> V
NS -> B
OH -> N
KC -> H
HV -> F
HF -> B
HP -> S
CB -> P
PN -> S
BK -> K
PF -> N
SO -> P
CF -> B
VO -> C
OO -> K
FC -> F
NV -> F
OK -> K
NN -> O
NO -> O
BP -> O
KB -> O
KF -> O"""

raw = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def init():
    polymer, substitutions = raw.split("\n\n")
    substitutions = [line.split(" -> ") for line in substitutions.splitlines()]
    substitutions = {pair: char for pair, char in substitutions}
    return polymer, substitutions


def build_cache(substitutions, depth):
    cache = dict()
    for pair in substitutions:
        polymer = pair
        for ii in range(depth):
            polymer = splice_polymer(polymer, substitutions)
        cache[pair] = "".join(polymer)
    return cache


def splice_polymer(polymer, substitutions):
    right = deque(polymer)
    left = deque(right.popleft())
    for rr in right:
        ll = left[-1]
        if middle := substitutions.get(ll + rr):
            left.append(middle)
        left.append(rr)
    return left


def get_pairs(string):
    return [f"{string[ii]}{string[ii + 1]}" for ii in range(len(string) - 1)]


def expand(polymer, cache):
    pairs = get_pairs(polymer)
    expanded_pairs = [cache.get(pair, pair) for pair in pairs]

    def foo(left, right):
        return left[:-1] + right

    whole = reduce(foo, expanded_pairs)
    return whole


def solver(polymer, substitutions, depth, cache_depth):
    cache = build_cache(substitutions, depth=cache_depth)
    for ii in range(depth):
        polymer = expand(polymer, cache)
        print(f"{ii=}")
        # print(f"{polymer=}")
    return polymer


def count(polymer):
    return {char: polymer.count(char) for char in set(polymer)}


_, substitutions = init()


def recursive(polymer, depth):
    # base case
    if depth == 0:
        return Counter(polymer)
    # recursive case
    else:
        counts = Counter()
        for ii, pair in enumerate(get_pairs(polymer)):
            spliced = splice_polymer(pair, substitutions)
            new_counts = recursive(spliced, depth - 1)
            # pop leftmost char to avoid fence post errors
            if ii != 0:
                left = pair[0]
                new_counts[left] -= 1
            counts += new_counts
    return counts


def part1():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    counts = recursive(polymer, depth=10)
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


def part2():
    t1 = time.time()

    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    counts = recursive(polymer, depth=20)
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    t2 = time.time()
    print(f"time: {t2-t1}")
    return max_count - min_count


if __name__ == "__main__":
    # p1 = part1()
    # print(f"part1: {p1}")
    # assert p1 == 1588
    p2 = part2()
    assert p2 == 1961318
    print(f"part2: {p2}")
