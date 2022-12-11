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
    divisor: int
    if_false: int
    if_true: int
    count: int = 0

    def throw(self, monkeys: list["Monkey"]):
        item = self.inventory.pop(0)
        item = self.operation(item)
        item = self.decrease_worry(item)
        result = self.test(item)
        monkey_id = self.if_true if result is True else self.if_false
        monkey = next(m for m in monkeys if m.id == monkey_id)
        monkey.inventory.append(item)
        self.count += 1

    def test(self, number: int) -> bool:
        return number % self.divisor == 0

    def decrease_worry(self, number: int) -> int:
        return number // 3


def example_monkeys():
    return [
        dict(
            id=0,
            inventory=[79, 98],
            operation=lambda worry: worry * 19,
            divisor=23,
            if_true=2,
            if_false=3,
        ),
        dict(
            id=1,
            inventory=[54, 65, 75, 74],
            operation=lambda worry: worry + 6,
            divisor=19,
            if_true=2,
            if_false=0,
        ),
        dict(
            id=2,
            inventory=[79, 60, 97],
            operation=lambda worry: worry * worry,
            divisor=13,
            if_true=1,
            if_false=3,
        ),
        dict(
            id=3,
            inventory=[74],
            operation=lambda worry: worry + 3,
            divisor=17,
            if_true=0,
            if_false=1,
        ),
    ]


def real_monkeys():
    return [
        dict(
            id=0,
            inventory=[83, 88, 96, 79, 86, 88, 70],
            operation=lambda worry: worry * 5,
            divisor=11,
            if_true=2,
            if_false=3,
        ),
        dict(
            id=1,
            inventory=[59, 63, 98, 85, 68, 72],
            operation=lambda worry: worry * 11,
            divisor=5,
            if_true=4,
            if_false=0,
        ),
        dict(
            id=2,
            inventory=[90, 79, 97, 52, 90, 94, 71, 70],
            operation=lambda worry: worry + 2,
            divisor=19,
            if_true=5,
            if_false=6,
        ),
        dict(
            id=3,
            inventory=[97, 55, 62],
            operation=lambda worry: worry + 5,
            divisor=13,
            if_true=2,
            if_false=6,
        ),
        dict(
            id=4,
            inventory=[74, 54, 94, 76],
            operation=lambda worry: worry * worry,
            divisor=7,
            if_true=0,
            if_false=3,
        ),
        dict(
            id=5,
            inventory=[58],
            operation=lambda worry: worry + 4,
            divisor=17,
            if_true=7,
            if_false=1,
        ),
        dict(
            id=6,
            inventory=[66, 63],
            operation=lambda worry: worry + 6,
            divisor=2,
            if_true=7,
            if_false=5,
        ),
        dict(
            id=7,
            inventory=[56, 56, 90, 96, 68],
            operation=lambda worry: worry + 7,
            divisor=3,
            if_true=4,
            if_false=1,
        ),
    ]


@utils.profile
def part1():
    monkeys = [Monkey(**data) for data in real_monkeys()]
    for round in range(20):
        for monkey in monkeys:
            while monkey.inventory:
                monkey.throw(monkeys)

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


@utils.profile
def part2():
    monkey_data = real_monkeys()
    modulus = 1
    for m in monkey_data:
        modulus *= m["divisor"]

    @dataclass
    class Monkey2(Monkey):
        def decrease_worry(self, number: int) -> int:
            return number % modulus

    monkeys = [Monkey2(**data) for data in monkey_data]
    for round in range(10000):
        for monkey in monkeys:
            while monkey.inventory:
                monkey.throw(monkeys)

    for m in monkeys:
        print(f"Monkey {m.id} inspected items {m.count} times")
    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


if __name__ == "__main__":
    assert part1() == 64032
    assert part2() == 12729522272
