import re

from typing_extensions import NamedTuple

import utils


class Range(NamedTuple):
    start: int
    stop: int

    def contains(self, value: int) -> bool:
        return self[0] <= value <= self[1]


Transform = dict[Range, Range]


@utils.profile
def part1(input: str):
    seeds, transforms = _parse_input(input)

    lowest = seeds[0]
    for seed in seeds:
        seed = _calculate_seed(seed, transforms)
        if seed < lowest:
            lowest = seed
    return lowest


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

    new = set()
    for pt in critical_points:
        if any(sr.contains(pt) for sr in seed_ranges):
            new.add(pt)
    critical_points = new

    results = []
    for seed in critical_points:
        seed = _calculate_seed(seed, transforms)
        results.append(seed)
    return min(results)


def _find_critical_points(transforms: list[Transform]) -> set[int]:
    critical_points = set()
    # working backwards from the rightmost transform
    for trans in reversed(transforms):
        # for any existing critical points;
        # if they intersect this transform, then transform the
        # points "left". Otherwise just leave them as-is.
        new = set()
        for pt in critical_points:
            pt_transformed_left = _apply_map_backwards(pt, trans)
            new.add(pt_transformed_left)
        critical_points = new

        # all the edges of the input ranges are automatically critical points
        for input_range in trans:
            critical_points.add(input_range[0])
            critical_points.add(input_range[1])
    return critical_points


def _calculate_seed(seed: int, transforms: list[Transform]) -> int:
    for transform in transforms:
        seed = _apply_map(seed, transform)
    return seed


def _apply_map(input: int, transform: Transform) -> int:
    for in_range, out_range in transform.items():
        if in_range.contains(input):
            offset = input - in_range.start
            return out_range.start + offset
    # if no ranges match, output = input
    return input


def _apply_map_backwards(input: int, transform: Transform) -> int:
    for in_range, out_range in transform.items():
        if out_range.contains(input):
            offset = input - out_range[0]
            return in_range[0] + offset
    return input


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
