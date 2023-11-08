import re
from itertools import product

import utils


def init(raw_string):
    instructions = []
    for line in raw_string.splitlines():
        onoff, range_strings = line.split(" ")
        range_strings = range_strings.split(",")
        ranges = []
        for string in range_strings:
            start, stop = list(map(int, re.findall("[-\d]+", string)))
            ranges.append(Range(start, stop + 1))
        shape = Shape(*ranges)
        instructions.append([onoff, shape])
    return instructions


def galaxy_brain(instructions):
    reactor = set()
    for onoff, new_shape in instructions:
        overlappers = {shape for shape in reactor if shape.overlaps(new_shape)}
        reactor = reactor.difference(overlappers)
        for shape in overlappers:
            shattered_shape = shape.difference(new_shape)
            reactor = reactor.union(shattered_shape)

        if onoff == "on":
            reactor.add(new_shape)

    return sum(shape.count() for shape in reactor)


@utils.profile
def part1(raw: str):
    instructions = [
        (onoff, shape)
        for onoff, shape in init(raw)
        if all(axis.overlaps(Range(-50, 50)) for axis in shape.axes)
    ]
    return galaxy_brain(instructions)


class RangeError(Exception):
    pass


class ShapeError(Exception):
    pass


class Range(tuple):
    def __new__(cls, start, stop):
        return super().__new__(cls, [start, stop])

    def __init__(self, start, stop):
        if stop < start:
            raise RangeError(f"stop must > start! {stop=}, {start=}")

    def __repr__(self) -> str:
        return f"Range({self.start}..{self.stop})"

    def __contains__(self, o: object) -> bool:
        return o in range(self.start, self.stop)

    def contains(self, o: "Range"):
        return (self.start < o.start < self.stop, self.start < o.stop < self.stop)

    def get_overlaps(self, o: "Range") -> list:
        if not any(self.contains(o)) and not any(o.contains(self)):
            return []
        return [max(self.start, o.start), min(self.stop, o.stop)]

    def overlaps(self, o: "Range") -> bool:
        return bool(self.get_overlaps(o))

    def split(self, *breakpoints):
        current = self
        new = []
        for bp in breakpoints:
            if bp in (self.start, self.stop):
                continue
            if bp not in self:
                raise RangeError(f"breakpoint {bp} not in {self}")
            new_range = Range(current.start, bp)
            if new_range.start != new_range.stop:
                new.append(new_range)
            current = Range(bp, self.stop)
        new.append(current)
        return new

    @property
    def start(self):
        return self[0]

    @property
    def stop(self):
        return self[1]


class Shape(tuple):
    def __new__(cls, *axes: Range):
        return super().__new__(cls, axes)

    def __init__(self, *axes: Range):
        if len(axes) < 2:
            raise ShapeError("You need to specify at least 2 axes")
        self.axes = axes

    def __repr__(self) -> str:
        return (
            "Shape("
            + ", ".join(
                f"{axisname}={axis.start}..{axis.stop}" for axisname, axis in zip("xyz", self.axes)
            )
            + ")"
        )

    def shatter(self, shape):
        overlaps = self.get_overlaps(shape)
        new_me = self.split(*overlaps)
        new_other = shape.split(*overlaps)
        return new_me, new_other

    def union(self, shape):
        my_pieces, other_pieces = self.shatter(shape)
        return set(my_pieces).union(set(other_pieces))

    def difference(self, shape):
        my_pieces, other_pieces = self.shatter(shape)
        return set(my_pieces).difference(set(other_pieces))

    def split(self, x_breaks, y_breaks=None, z_breaks=None):
        y_breaks = y_breaks or []
        z_breaks = z_breaks or []
        breakpoints = [x_breaks, y_breaks, z_breaks]
        new_axes = [axis.split(*breaks) for axis, breaks in zip(self.axes, breakpoints)]
        return {Shape(*axes) for axes in product(*new_axes)}

    def count(self):
        prod = 1
        for axis in self.axes:
            length = abs(axis.stop - axis.start)
            prod *= length
        return prod

    def get_overlaps(self, shape):
        return [mine.get_overlaps(other) for mine, other in zip(self.axes, shape.axes)]

    def overlaps(self, shape):
        return all(map(bool, self.get_overlaps(shape)))


@utils.profile
def part2(raw: str):
    instructions = init(raw)
    return galaxy_brain(instructions)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day22")
    assert part1(raw) == 533863
    assert part2(raw) == 1261885414840992
