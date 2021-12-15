import functools
import time
from collections import deque, Counter

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

# raw = """NNCB
#
# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C"""


def init():
    polymer, substitutions = raw.split("\n\n")
    substitutions = [line.split(" -> ") for line in substitutions.splitlines()]
    substitutions = {pair: char for pair, char in substitutions}
    return polymer, substitutions


polymer, substitutions = init()


def get_pairs(string):
    return [f"{string[ii]}{string[ii + 1]}" for ii in range(len(string) - 1)]


def galaxy_brain(polymer, depth):
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
            expanded = pair[0] + middle + pair[-1]
            new_pairs += {key: value * count for key, value in Counter(get_pairs(expanded)).items()}
        pairs = new_pairs

    most_common = totals.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


def part1():
    return galaxy_brain(polymer, depth=10)


def part2():
    return galaxy_brain(polymer, depth=40)


if __name__ == "__main__":
    p1 = part1()
    print(f"part1: {p1}")
    assert p1 == 2590
    p2 = part2()
    print(f"part2: {p2}")
    assert p2 == 2875665202438
