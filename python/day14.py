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


def splice_polymer(pair, char, polymer):
    joiner = pair[0] + char + pair[1]
    components = polymer.split(pair)
    result = joiner.join(components)
    return result


def splice_polymer2(polymer, substitutions):
    new_polymer = ""
    for ii, char in enumerate(polymer):
        try:
            next_char = polymer[ii + 1]
        except IndexError:
            break
        pair = char + next_char
        if pair in substitutions:
            new_polymer += pair[0] + substitutions[pair]
            # print(f"after matching {pair}, {new_polymer=}")
        else:
            new_polymer += pair[0]
    new_polymer += pair[1]
    return new_polymer


def count(polymer):
    return {char: polymer.count(char) for char in set(polymer)}


def part1():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    for ii in range(10):
        polymer = splice_polymer2(polymer, substitutions)
        print(f"{polymer=}")

    counts = count(polymer)
    min_count = min(counts.values())
    max_count = max(counts.values())
    return max_count - min_count


def part2():
    polymer, substitutions = init()
    for ii in range(40):
        print(f"{ii=}")
        polymer = splice_polymer2(polymer, substitutions)

    counts = count(polymer)
    min_count = min(counts.values())
    max_count = max(counts.values())
    return max_count - min_count


if __name__ == "__main__":
    p1 = part1()
    print(f"part1: {p1}")
    p2 = part2()
    print(f"part2: {p2}")
