import time
from collections import deque

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


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.first = node
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    @property
    def nodes(self):
        node = self.first
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        return nodes

    def __repr__(self):
        return f"[{', '.join(map(str, self.nodes))}]"

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __next__(self):
        node = self.head
        if self.head.next is not None:
            self.head = self.head.next
        else:
            raise StopIteration
        return node


def splice_polymer(polymer, substitutions):
    right = deque(polymer)
    left = deque(right.popleft())
    for rr in right:
        ll = left[-1]
        if middle := substitutions.get(ll + rr):
            left.append(middle)
        left.append(rr)
    return left


def count(polymer):
    return {char: polymer.count(char) for char in set(polymer)}


def part1():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    for ii in range(10):
        polymer = splice_polymer(polymer, substitutions)

    counts = count(polymer)
    min_count = min(counts.values())
    max_count = max(counts.values())
    return max_count - min_count


def part2():
    polymer, substitutions = init()
    print(f"before anything: {polymer=}")
    t1 = time.time()
    for ii in range(20):
        print(f"{ii=}")
        polymer = splice_polymer(polymer, substitutions)

    counts = count(polymer)
    min_count = min(counts.values())
    max_count = max(counts.values())
    t2 = time.time()
    print(f"time: {t2-t1}")
    return max_count - min_count


if __name__ == "__main__":
    p1 = part1()
    print(f"part1: {p1}")
    # assert p1 == 2590
    p2 = part2()
    print(f"part2: {p2}")
