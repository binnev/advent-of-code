import re
from dataclasses import dataclass
from functools import reduce
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


monkey_rx = """Monkey (\d):
  Starting items: (.*)
  Operation: new = (.*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d)
    If false: throw to monkey (\d)"""


def parse_monkey(monkey_str: str) -> dict:
    rx = re.compile(monkey_rx)
    match = rx.search(monkey_str)
    id, items, operation, divisor, if_true, if_false = match.groups()
    match operation.split():
        case ["old", "*", "old"]:
            operation = lambda old: old * old
        case ["old", "*", number]:
            operation = lambda old: old * int(number)
        case ["old", "+", number]:
            operation = lambda old: old + int(number)

    return dict(
        id=int(id),
        inventory=list(map(int, items.split(", "))),
        operation=operation,
        divisor=int(divisor),
        if_true=int(if_true),
        if_false=int(if_false),
    )


def parse_input(input: str) -> list[dict]:
    return list(map(parse_monkey, input.split("\n\n")))


@dataclass
class Monkey:
    id: int
    inventory: list[int]
    operation: Callable  # changes worry level
    divisor: int
    if_false: int
    if_true: int
    count: int = 0

    def throw(self, item: int, monkeys: list["Monkey"]):
        item = self.operation(item)
        item = self.decrease_worry(item)
        result = item % self.divisor == 0
        monkey_id = self.if_true if result else self.if_false
        monkey = next(m for m in monkeys if m.id == monkey_id)
        monkey.inventory.append(item)
        self.count += 1

    def decrease_worry(self, number: int) -> int:
        return number // 3


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day11")
    monkey_data = parse_input(input)
    monkeys = [Monkey(**data) for data in monkey_data]

    for round in range(20):
        for monkey in monkeys:
            for item in monkey.inventory:
                monkey.throw(item, monkeys)
            monkey.inventory = []

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


@utils.profile
def part2():
    """
    Use clock arithmetic to keep the worry numbers low, while still allowing the "is divisible by
    x" calculations to give the same result. For all monkeys' calculations to be unaffected,
    the max value of the clock should be the lowest common multiple of all the monkeys' divisors.
    Because the divisors are all prime, the lowest common multiple is simply the product.
    """

    input = utils.load_puzzle_input("2022/day11")
    monkey_data = parse_input(input)
    modulus = reduce(lambda a, b: a * b, (m["divisor"] for m in monkey_data))

    @dataclass
    class ModuloMonkey(Monkey):
        def decrease_worry(self, number: int) -> int:
            return number % modulus

    monkeys = [ModuloMonkey(**data) for data in monkey_data]
    for round in range(10000):
        for monkey in monkeys:
            for item in monkey.inventory:
                monkey.throw(item, monkeys)
            monkey.inventory = []

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


if __name__ == "__main__":
    assert part1() == 64032
    assert part2() == 12729522272
