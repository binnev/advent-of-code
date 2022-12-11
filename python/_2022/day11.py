from dataclasses import dataclass
from typing import Callable

from python import utils

example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass
class Monkey:
    id: int
    inventory: list[int]
    operation: Callable  # changes worry level
    test: Callable  # checks where it should throw item
    if_false: int
    if_true: int
    count: int = 0

    def throw(self, monkeys: list["Monkey"]):
        item = self.inventory.pop(0)
        item = self.operation(item)
        item = item // 3
        result = self.test(item)
        monkey_id = self.if_true if result is True else self.if_false
        # worry level decreases
        monkey = next(m for m in monkeys if m.id == monkey_id)
        monkey.inventory.append(item)
        self.count += 1


def example_monkeys():
    return [
        Monkey(
            id=0,
            inventory=[79, 98],
            operation=lambda worry: worry * 19,
            test=lambda worry: worry % 23 == 0,
            if_true=2,
            if_false=3,
        ),
        Monkey(
            id=1,
            inventory=[54, 65, 75, 74],
            operation=lambda worry: worry + 6,
            test=lambda worry: worry % 19 == 0,
            if_true=2,
            if_false=0,
        ),
        Monkey(
            id=2,
            inventory=[79, 60, 97],
            operation=lambda worry: worry * worry,
            test=lambda worry: worry % 13 == 0,
            if_true=1,
            if_false=3,
        ),
        Monkey(
            id=3,
            inventory=[74],
            operation=lambda worry: worry + 3,
            test=lambda worry: worry % 17 == 0,
            if_true=0,
            if_false=1,
        ),
    ]


def real_monkeys():
    return [
        Monkey(
            id=0,
            inventory=[83, 88, 96, 79, 86, 88, 70],
            operation=lambda worry: worry * 5,
            test=lambda worry: worry % 11 == 0,
            if_true=2,
            if_false=3,
        ),
        Monkey(
            id=1,
            inventory=[59, 63, 98, 85, 68, 72],
            operation=lambda worry: worry * 11,
            test=lambda worry: worry % 5 == 0,
            if_true=4,
            if_false=0,
        ),
        Monkey(
            id=2,
            inventory=[90, 79, 97, 52, 90, 94, 71, 70],
            operation=lambda worry: worry + 2,
            test=lambda worry: worry % 19 == 0,
            if_true=5,
            if_false=6,
        ),
        Monkey(
            id=3,
            inventory=[97, 55, 62],
            operation=lambda worry: worry + 5,
            test=lambda worry: worry % 13 == 0,
            if_true=2,
            if_false=6,
        ),
        Monkey(
            id=4,
            inventory=[74, 54, 94, 76],
            operation=lambda worry: worry * worry,
            test=lambda worry: worry % 7 == 0,
            if_true=0,
            if_false=3,
        ),
        Monkey(
            id=5,
            inventory=[58],
            operation=lambda worry: worry + 4,
            test=lambda worry: worry % 17 == 0,
            if_true=7,
            if_false=1,
        ),
        Monkey(
            id=6,
            inventory=[66, 63],
            operation=lambda worry: worry + 6,
            test=lambda worry: worry % 2 == 0,
            if_true=7,
            if_false=5,
        ),
        Monkey(
            id=7,
            inventory=[56, 56, 90, 96, 68],
            operation=lambda worry: worry + 7,
            test=lambda worry: worry % 3 == 0,
            if_true=4,
            if_false=1,
        ),
    ]


@utils.profile
def part1():
    monkeys = real_monkeys()
    for round in range(20):
        for monkey in monkeys:
            while monkey.inventory:
                monkey.throw(monkeys)

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    part1()
    part2()
