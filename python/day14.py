import functools
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
            polymer = expand(polymer, substitutions)
        cache[pair] = "".join(polymer)
    return cache


polymer, substitutions = init()


def simple_cache(func):
    cache = dict()

    @functools.wraps(func)
    def inner(*args):
        result = func(*args)
        cache[args] = result
        return result

    inner.cache = cache
    return inner


def expand(polymer):
    """This expands the string by depth 1. This is the fastest thing I got right now..."""
    right = deque(polymer)
    ll = right.popleft()
    left = deque(ll)
    for rr in right:
        if middle := substitutions.get(ll + rr):
            left.append(middle)
        left.append(rr)
        ll = rr
    return "".join(left)


def get_pairs(string):
    return [f"{string[ii]}{string[ii + 1]}" for ii in range(len(string) - 1)]


def recursive_simple(polymer, depth):
    # base case
    if depth == 0:
        return Counter(polymer)
    # recursive case
    return Counter(recursive_simple(expand(polymer), depth - 1))


def recursive_by_pairs(polymer, depth):
    # base case
    if depth == 0:
        return Counter(polymer)
    # recursive case
    counts = Counter()
    for ii, pair in enumerate(get_pairs(polymer)):
        spliced = expand(pair)
        new_counts = recursive_by_pairs(spliced, depth - 1)
        # pop leftmost char to avoid fence post errors
        if ii != 0:
            left = pair[0]
            new_counts[left] -= 1
        counts += new_counts
    return counts


def hungry_caterpillar(polymer, depth):
    totals = Counter()
    for ii, pair in enumerate(get_pairs(polymer)):
        counts = Counter(dead_simple(pair, depth))
        # pop leftmost char to avoid fence post errors
        if ii != 0:
            left = pair[0]
            counts[left] -= 1
        totals += counts
    return totals


def dead_simple(polymer, depth):
    """Generate the whole string and then count the elements"""
    for ii in range(depth):
        polymer = expand(polymer)
    return Counter(polymer)


"""
ideas: 

the problem grows with approx 4 * 1.94**depth
for depth=40 that's a 1,300,556,393,886 length string.
I need to be 1) not holding all that in memory, and 
2) caching function calls to not do all that work 

feed the whole string left<- into the function and expand it as it comes.
Have the function "eat" the string pair by pair, and return the 40-deep counts for all the pairs.
That way we never have to store the whole string. 
Or keep expanding until the chunk you're working on is a certain length, then recurse with less 
depth
for depth = 2: 
queue = ABC
A-N-BC
A-M-N-O-BC
counts += Counter(A-M-N-O-)
queue = BC
B-Z-C
B-X-Z-Y-C
counts += Counter(B-X-Z-Y-)
queue = C
counts += Counter(C)

transform the substitutions dict into a tree. Then just iterate over the tree and add the nodes (
(e.g. "NB") to the counter, instead of building up the whole string. 


don't worry about the order? 
polymer = ABCD
can be represented as 
{
  AB: 1,
  BC: 1, 
  CD: 1,
}
to go down 1 depth, iterate over the keys 
    1. expand each key by 1 e.g. AB -> AXB
    2. get the counts of the pairs: 
       {AX: 1, XB: 1}
    3. multiply those counts by the number of times AB occurred
    4. add the result to the total counts
    

"""


def tests():
    solver_functions = [
        dead_simple,
        # recursive_by_pairs,
        recursive_simple,
        hungry_caterpillar,
    ]
    print("tests")
    for func in solver_functions:
        print(f"\t{func.__name__}: ", end="")
        assert func(polymer, depth=0) == Counter("NNCB")
        assert func(polymer, depth=1) == Counter("NCNBCHB")
        assert func(polymer, depth=2) == Counter("NBCCNBBBCBHCB")
        assert func(polymer, depth=3) == Counter("NBBBCNCCNBBNBNBBCHBHHBCHB")
        assert func(polymer, depth=4) == Counter(
            "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
        )
        print("passed")

    depth = 22
    print("")
    print(f"profiling w. {depth=}")
    for func in solver_functions:
        print(f"\t{func.__name__}: ", end="")
        t1 = time.time()
        func(polymer, depth=depth)
        t2 = time.time()
        print(f"time={t2-t1}")


def part1():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    assert dead_simple(polymer, depth=0) == Counter("NNCB")
    assert dead_simple(polymer, depth=1) == Counter("NCNBCHB")
    assert dead_simple(polymer, depth=2) == Counter("NBCCNBBBCBHCB")
    assert dead_simple(polymer, depth=3) == Counter("NBBBCNCCNBBNBNBBCHBHHBCHB")
    assert dead_simple(polymer, depth=4) == Counter(
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )
    t1 = time.time()
    counts = dead_simple(polymer, depth=20)
    t2 = time.time()
    print(f"{t2-t1=}")
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    return max_count - min_count


def part2():
    t1 = time.time()

    polymer, substitutions = init()
    cache = build_cache(substitutions, depth=10)
    print(f"before anything: {polymer=}")
    counts = recursive_simple(polymer, depth=4, cache=cache)
    most_common = counts.most_common()
    min_count = most_common[-1][1]
    max_count = most_common[0][1]
    t2 = time.time()
    print(f"time: {t2-t1}")
    return max_count - min_count


if __name__ == "__main__":
    tests()
    # p1 = part1()
    # print(f"part1: {p1}")
    # assert p1 == 1588
    # p2 = part2()
    # assert p2 == 1961318  # for 20 reps
    # print(f"part2: {p2}")
