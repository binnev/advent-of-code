import itertools
import re

import utils

Match = tuple[int, int]  # the start/end indices of a substring within a string


@utils.profile
def part1(input: str) -> int:
    parsed = parse_input(input)
    result = 0
    for springs, numbers in parsed:
        possible_arrangements = elegant(springs, numbers)
        result += len(possible_arrangements)
    return result


@utils.profile
def part2(input: str):
    parsed = parse_input(input)
    parsed = [unfold(springs, numbers) for springs, numbers in parsed]
    result = 0
    for springs, numbers in parsed:
        possible_arrangements = elegant(springs, numbers)
        result += len(possible_arrangements)
    return result


def unfold(springs: str, numbers: list[int]) -> tuple[str, list[int]]:
    new_springs = "?".join([springs] * 5)
    new_numbers = numbers * 5
    return new_springs, new_numbers


def brute(line: str, numbers: list[int]) -> list[str]:
    """
    Brute force compute the combinations of hash placements.
    Filter out the ones that don't satisfy the numbers.
    As expected, scales extremely poorly.
    """

    def substitute(s: str, indices: list[int]) -> str:
        chars = list(s)
        for ii in indices:
            chars[ii] = "#"
        # remove question marks -- they are empty now
        for ii in range(len(chars)):
            if chars[ii] == "?":
                chars[ii] = "."
        return "".join(chars)

    hashes_needed = sum(numbers)
    hashes_found = line.count("#")
    hashes_to_place = hashes_needed - hashes_found

    question_mark_locations = [ii for ii, char in enumerate(line) if char == "?"]

    results = [
        substitute(line, indices)
        for indices in itertools.combinations(question_mark_locations, hashes_to_place)
    ]
    results = [result for result in results if satisfies_pattern(result, numbers)]
    return results


def sub_hashes(s: str, left: int, right: int) -> str:
    # don't forget to delete the left ?s
    chars = list(s)
    for ii, char in enumerate(chars):
        if ii < left:
            if char == "?":
                char = "."
        elif left <= ii < right:
            char = "#"
        else:
            break  # don't process chars to the right of the substring
        chars[ii] = char
    return "".join(chars)


def elegant(line: str, numbers: list[int], start: int = 0, depth: int = 0):
    # base case
    hashes_so_far = re.findall(r"#+", line)
    groups_so_far = list(map(len, hashes_so_far))
    if groups_so_far == numbers:
        return [line.replace("?", ".")]

    number = numbers[depth]
    line_length = len(line)

    branches = []
    for right in range(number + start, len(line) + 1):
        left = right - number
        substr = line[left:right]
        if ("?" not in substr) and ("#" not in substr):
            continue
        from_start = line[:right]
        to_end = line[left:]
        if "?" not in to_end:  # todo: not sure this doesn't break things
            continue
        prev_char = "^" if left == 0 else line[left - 1]
        next_char = "$" if right == line_length else line[right]
        groups_so_far = re.findall(r"#+", from_start)
        should_branch = (
            next_char != "#"
            and prev_char != "#"
            and (substr.count("#") + substr.count("?")) == number
        )
        should_break = groups_so_far == numbers[: depth + 1]
        if should_branch:
            new_substr = sub_hashes(line, left, right)
            start = right
            branches.append((start, new_substr))
        if should_break:
            break

    results = []
    for start, substr in branches:
        intermediate = elegant(substr, numbers, start=start, depth=depth + 1)
        results.extend(intermediate)
    return results


def parse_input(input: str) -> list[tuple[str, list[int]]]:
    result = []
    for line in input.splitlines():
        springs, numbers = line.split()
        numbers = list(map(int, numbers.split(",")))
        result.append((springs, numbers))
    return result


def satisfies_pattern(s: str, numbers: list[int]) -> bool:
    hash_groups = re.findall(r"#+", s)
    lengths = list(map(len, hash_groups))
    return lengths == numbers


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day12")
    part2(input)
