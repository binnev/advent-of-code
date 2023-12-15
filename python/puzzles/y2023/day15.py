import re
from pprint import pprint

from typing import NamedTuple

import utils


class Lens(NamedTuple):
    label: str
    focal_length: int

    def __str__(self):
        return f"[{self.label} {self.focal_length}]"

    # def __repr__(self):
    #     return self.__str__()


HashMap = list[list[Lens]]


@utils.profile
def part1(input: str):
    steps = parse_input(input)
    return sum(map(hash, steps))


@utils.profile
def part2(input: str):
    steps = parse_input(input)
    hashmap = build_hashmap(steps)
    return calc_focusing_power(hashmap)


def calc_focusing_power(hashmap: HashMap) -> int:
    """
    One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.
    """
    result = 0
    for box_number in range(256):
        box = hashmap[box_number]
        for slot, lens in enumerate(box):
            slot += 1  # 1-based counting
            result += (box_number + 1) * slot * lens.focal_length
    return result


def build_hashmap(steps: list[str]) -> HashMap:
    hashmap: HashMap = [[] for _ in range(256)]
    assert len(hashmap) == 256
    for step in steps:
        box, label, operator, focal_length = parse_step(step)
        if operator == "-":
            remove(box_contents=hashmap[box], label=label)
        elif operator == "=":
            focal_length = int(focal_length)
            insert(box_contents=hashmap[box], lens=Lens(label=label, focal_length=focal_length))
        else:
            raise Exception("panik!!")

        # print("")
        # print(f'After "{step}":')
        # for ii, box in enumerate(hashmap):
        #     if box:
        #         stringified = " ".join(map(str, box))
        #         print(f"Box {ii}: {stringified}")

    return hashmap


def insert(box_contents: list[Lens], lens: Lens):
    # If there is already a lens in the box with the same label, replace the old lens with the
    # new lens
    if any(l.label == lens.label for l in box_contents):
        matching_lens = next(l for l in box_contents if l.label == lens.label)
        ind = box_contents.index(matching_lens)
        box_contents[ind] = lens
    # If there is not already a lens in the box with the same label, add the lens to the box
    # immediately behind any lenses already in the box.
    else:
        box_contents.append(lens)


def remove(box_contents: list[Lens], label: str):
    # "If no lens in that box has the given label, nothing happens."
    if any(l.label == label for l in box_contents):
        matching_lens = next(l for l in box_contents if l.label == label)
        box_contents.remove(matching_lens)


def parse_step(step: str) -> tuple[int, str, str, str]:
    rx = re.compile(r"(\w+)([-|=])(\w*)")
    match = rx.match(step)
    if not match:
        raise Exception(f"Couldn't find a match for step {step}")
    label, operator, focal_length = match.groups()
    box = hash(label)
    return box, label, operator, focal_length


def hash(input: str) -> int:
    result = 0
    for char in input:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def parse_input(input: str) -> list[str]:
    # puzzle says to ignore newlines; better safe than sorry
    return input.strip().split(",")


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day15")
    part2(input)
