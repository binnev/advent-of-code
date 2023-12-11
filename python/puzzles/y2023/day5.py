import re

from typing import NamedTuple

import utils


class Range(NamedTuple):
    start: int
    stop: int

    def contains(self, value: int) -> bool:
        return self[0] <= value <= self[1]


class Transform(dict[Range, Range]):
    def forwards(self, value: int) -> int:
        for in_range, out_range in self.items():
            if in_range.contains(value):
                offset = value - in_range.start
                return out_range.start + offset
        # if no ranges match, output = value
        return value

    def backwards(self, value: int) -> int:
        for in_range, out_range in self.items():
            if out_range.contains(value):
                offset = value - out_range[0]
                return in_range[0] + offset
        return value


@utils.profile
def part1(input: str):
    seeds, transforms = _parse_input(input)
    return min(_apply_transforms(seed, transforms) for seed in seeds)


@utils.profile
def part2(input: str):
    seeds, transforms = _parse_input(input)
    seed_ranges = []
    for ii in range(0, len(seeds) // 2 + 1, 2):
        start = seeds[ii]
        width = seeds[ii + 1]
        seed_range = Range(start, start + width - 1)
        seed_ranges.append(seed_range)

    critical_points = _find_critical_points(transforms)
    for start, end in seed_ranges:
        critical_points.add(start)
        critical_points.add(end)

    # filter out any critical points that aren't within the input ranges
    critical_points = filter(lambda pt: any(r.contains(pt) for r in seed_ranges), critical_points)

    return min(_apply_transforms(seed, transforms) for seed in critical_points)


def _find_critical_points(transforms: list[Transform]) -> set[int]:
    critical_points = set()
    # working backwards from the rightmost transform
    for trans in reversed(transforms):
        # for any existing critical points;
        # if they intersect this transform, then transform the
        # points "left". Otherwise just leave them as-is.
        new = set()
        for pt in critical_points:
            new.add(trans.backwards(pt))
        critical_points = new

        # all the edges of the input ranges are automatically critical points
        for input_range in trans:
            critical_points.add(input_range[0])
            critical_points.add(input_range[1])
    return critical_points


def _apply_transforms(seed: int, transforms: list[Transform]) -> int:
    for transform in transforms:
        seed = transform.forwards(seed)
    return seed


def _parse_range_line(line: str) -> tuple[Range, Range]:
    dst, src, width = list(map(int, line.split()))
    src_range = Range(start=src, stop=src + width - 1)
    dst_range = Range(start=dst, stop=dst + width - 1)
    return src_range, dst_range


def _parse_input(input: str) -> tuple[list[int], list[Transform]]:
    lines = input.splitlines()
    seed_line = lines.pop(0)
    input = "\n".join(lines)
    seeds = list(map(int, re.findall(r"(\d+)", seed_line)))

    transform = None
    transforms = []
    for line in input.splitlines():
        if line.endswith("map:"):
            if transform:
                transforms.append(transform)
            transform = Transform()
        elif line.strip():
            src_range, dst_range = _parse_range_line(line)
            transform[src_range] = dst_range
    transforms.append(transform)

    return seeds, transforms
