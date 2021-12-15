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


_, substitutions = init()


def get_pairs(string):
    return [f"{string[ii]}{string[ii + 1]}" for ii in range(len(string) - 1)]


def galaxy_brain(polymer, depth):
    """
    don't worry about the order?
    polymer = ABC
    can be represented as
    pairs = {
      AB: 1,
      BC: 1,
    }
    initialise counts:
    totals = Counter(ABC) = {A: 1, B: 1, C: 1}
    to go down 1 depth, iterate over the pairs:
        pair = AB
        expand pair by 1 e.g. AB -> AXB
        increase the count of X by the number of times the pair is in pairs (1):
            totals = {A: 1, B: 1, C: 1, X: 1}
        2. get the counts of the pairs:
           {AX: 1, XB: 1}
        3. multiply those counts by the number of times AB occurred
        4. add the result to the total counts
    """
    totals = Counter(polymer)
    pairs = Counter(get_pairs(polymer))
    new_pairs = Counter()
    for ii in range(depth):
        for pair, count in pairs.items():
            if middle := substitutions.get(pair, ""):
                totals[middle] = totals.get(middle, 0) + count
            expanded = pair[0] + middle + pair[-1]
            new_pairs += {key: value * count for key, value in Counter(get_pairs(expanded)).items()}
        pairs = new_pairs
        new_pairs = Counter()
    return totals


def part1():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    counts = galaxy_brain(polymer, depth=10)
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


def part2():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    counts = galaxy_brain(polymer, depth=40)
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


if __name__ == "__main__":
    p1 = part1()
    print(f"part1: {p1}")
    assert p1 == 2590
    p2 = part2()
    print(f"part2: {p2}")
    assert p2 == 2875665202438
