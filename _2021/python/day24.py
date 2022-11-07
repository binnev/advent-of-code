import re
from itertools import combinations_with_replacement

from _2021.python import utils

raw = utils.load_puzzle_input("day24")


def init(raw_string):
    instructions = []
    for line in raw_string.splitlines():
        operation, *terms = line.split(" ")
        instructions.append((operation, tuple(terms)))
    return instructions


class AluError(Exception):
    pass


class Alu:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def __init__(self):
        self.instructions = init(raw)

    def parse(self, b):
        matches = re.findall("[-\d]+", b)
        return int(matches[0]) if matches else getattr(self, b)

    def inp(self, a: str, b: str):
        b = self.parse(b)
        setattr(self, a, b)

    def mul(self, a, b):
        b = self.parse(b)
        a_value = getattr(self, a)
        result = a_value * b
        setattr(self, a, result)

    def add(self, a, b):
        b = self.parse(b)
        a_value = getattr(self, a)
        result = a_value + b
        setattr(self, a, result)

    def div(self, a, b):
        b = self.parse(b)
        a_value = getattr(self, a)
        result = a_value // b
        setattr(self, a, result)

    def mod(self, a, b):
        b = self.parse(b)
        a_value = getattr(self, a)
        if a_value < 0 or b <= 0:
            raise AluError("mod can't handle that")
        result = a_value % b
        setattr(self, a, result)

    def eql(self, a, b):
        b = self.parse(b)
        a_value = getattr(self, a)
        result = int(a_value == b)
        setattr(self, a, result)

    def __repr__(self):
        w = self.w
        x = self.x
        y = self.y
        z = self.z
        return f"ALU({w=}, {x=}, {y=}, {z=})"

    def validate_model_number(self, model_number):
        digits = list(str(model_number))
        for operation, terms in self.instructions:
            terms = list(terms)
            if operation == "inp":
                terms += [digits.pop(0)]
            method = getattr(self, operation)
            method(*terms)
        return "0" not in str(self.z)

@utils.profile
def part1():
    alu = Alu()
    for ii, guess in enumerate(combinations_with_replacement(list(range(1, 10)), r=14)):
        guess = int("".join(map(str, guess)))
        success = alu.validate_model_number(guess)
        if ii % 100 == 0:
            print(f"guessing {guess}... {success}")


if __name__ == "__main__":
    part1()
