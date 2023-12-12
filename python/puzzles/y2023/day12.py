import re

import utils

Match = tuple[int, int]  # the start/end indices of a substring within a string


@utils.profile
def part1(input: str):
    ...


@utils.profile
def part2(input: str):
    ...
    return 0


def parse_input(input: str) -> list[tuple[str, list[int]]]:
    result = []
    for line in input.splitlines():
        springs, numbers = line.split()
        numbers = list(map(int, numbers.split(",")))
        result.append((springs, numbers))
    return result


def find_arrangements(springs: str, numbers: list[int]) -> list[str]:
    """
    Actually compute the arrangements so we can sanity check them. Try a recursive strategy where
    we find the possible positions for the first number, then pass the string and rest of the
    numbers to a recursive call.
    """

    # base case -- no more numbers -> return input string as-is
    if not numbers:
        return [springs]

    # recursive case
    number = numbers[0]
    # find the possible places this group *could* go -- patches of contiguous ?s at least N long
    # need to also catch non-contiguous ?s if they're joined by #s.
    possible_places = get_possible_places(springs, number)
    if not possible_places:
        return []

    # create new string for each arrangement
    new_strings = [substitute_hashes(springs, m) for m in possible_places]

    # # filter out ones that already don't satisfy the pattern
    # new_strings = [s for s in new_strings if satisfies_pattern(s, numbers)]

    # do recursion on these with the next first number
    results = []
    for s in new_strings:
        foo = find_arrangements(s, numbers[1:])
        results.extend(foo)

    return results


def substitute_hashes(s: str, m: Match) -> str:
    chars = list(s)
    for ii in range(m[0], m[1]):
        chars[ii] = "#"
    return "".join(chars)


def satisfies_pattern(s: str, numbers: list[int]) -> bool:
    hash_groups = re.findall(r"#+", s)
    lengths = list(map(len, hash_groups))
    return lengths == numbers


def is_match(s: str, length: int) -> bool:
    if len(s) < length:
        return False  # not enough characters left in string

    chars = s[:length]

    # for the lookahead
    try:
        next_char = s[length]
    except IndexError:
        next_char = "."

    if all(c in "?#" for c in chars) and next_char not in "#":
        return True
    return False


def get_possible_places(s: str, number: int) -> list[Match]:
    matches = []
    for ii in range(len(s)):
        substr = s[ii : ii + number]
        if ii > 0:
            prev_char = s[ii - 1]
        else:
            prev_char = "^"  # start of string

        try:
            next_char = s[ii + number]
        except IndexError:
            next_char = "$"  # end of string
        if all(char in "?" for char in substr) and next_char != "#" and prev_char != "#":
            matches.append((ii, ii + number))
    return matches


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day12")
    part1(input)
