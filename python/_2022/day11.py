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


def parse_monkey(monkey_str: str) -> dict:
    monkey_dict = dict()
    for line in monkey_str.split("\n"):
        line = line.strip()
        if line.startswith("Monkey"):
            monkey_dict["id"] = int(line.replace("Monkey ", "").replace(":", ""))
        elif line.startswith("Starting items: "):
            items = line.replace("Starting items: ", "")
            monkey_dict["inventory"] = list(map(int, items.split(", ")))
        elif line.startswith("Operation"):
            operation = line.replace("Operation: new = ", "")
            match operation.split():
                case ["old", "*", "old"]:
                    monkey_dict["operation"] = lambda old: old * old
                case ["old", "*", number]:
                    monkey_dict["operation"] = lambda old: old * int(number)
                case ["old", "+", number]:
                    monkey_dict["operation"] = lambda old: old + int(number)
        elif line.startswith("Test"):
            monkey_dict["divisor"] = int(line.replace("Test: divisible by ", ""))
        elif line.startswith("If true"):
            monkey_dict["if_true"] = int(line.replace("If true: throw to monkey ", ""))
        elif line.startswith("If false"):
            monkey_dict["if_false"] = int(line.replace("If false: throw to monkey ", ""))
    return monkey_dict


def parse_input(input: str) -> list[dict]:
    output = []
    for monkey_str in input.split("\n\n"):
        output.append(parse_monkey(monkey_str))
    return output


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


@utils.profile
def part1():
    input = utils.load_puzzle_input("2022/day11")
    monkey_data = parse_input(input)
    monkeys = [Monkey(**data) for data in monkey_data]
    for round in range(20):
        for monkey in monkeys:
            while monkey.inventory:
                monkey.throw(monkeys)

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


@utils.profile
def part2():
    input = utils.load_puzzle_input("2022/day11")
    monkey_data = parse_input(input)
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

    most_active = sorted(monkeys, key=lambda x: -x.count)
    return most_active[0].count * most_active[1].count


if __name__ == "__main__":
    assert part1() == 64032
    assert part2() == 12729522272
