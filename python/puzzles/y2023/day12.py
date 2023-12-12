import re

import utils


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
        return springs

    # recursive case
    number = numbers[0]
    # find the possible places this group *could* go -- patches of contiguous ?s at least N long
    # need to also catch non-contiguous ?s if they're joined by #s.
    # THIS IS  AJOB FOR REGEX!!

    # filter out ones that already don't satisfy the pattern
    # create new string for each arrangement, and do recursion on these

    # todo: error case -- no arrangements are possible (because caller chose a bad first
    #  arrangement)


Match = tuple[int, int]  # the start/end indices of a substring within a string


def _regex_magic(s: str) -> list[str]:
    """
    This substring jank is required because the regex on its own doesn't match overlapping values
    like "oneight". In this case the regex will only find "one", not "eight".
    """
    rx = re.compile("one|two|three|four|five|six|seven|eight|nine|[1-9]")
    matches = []
    for ii in range(len(s)):
        substr = s[ii:]
        if match := rx.match(substr):
            matches.append(match.group())
    return matches


# def get_possible_places(s: str, number: int) -> list[Match]:
#     # find all the groups of length "number" that consist solely of "?"s and "#"s
#     rx = re.compile(
#         r"^"  # match must start at the start of the string
#         r"([?#]{" + str(number) + r"})"  # capture exactly `number` ?# characters
#         r"(?=[?#])"  # only match if the next character is not ?#
#     )
#     r"Isaac (?=Asimov)"  # matches 'Isaac ' only if it's not followed by "Asimov"
#     matches = []
#     for ii in range(len(s)):
#         substr = s[ii:]
#         if match := rx.match(substr):
#             # indices = (match.pos + ii, match.lastindex + ii)
#             indices = tuple(m + ii for m in match.regs[1])
#             matches.append(indices)
#     return matches


# def is_match(s: str, length: int) -> bool:
#     rx = re.compile(
#         r"^"  # match must start at the start of the string
#         r"(#|\?{" + str(length) + r"})"  # capture exactly `number` ?# characters
#         r"$|^#|^\?"  # end of string or non-?# characters may follow
#         # r"(?=[?#])"  # only match if the next character is not ?#
#     )
#     if match := rx.match(s):
#         return True
#     return False


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
        if all(char in "#?" for char in substr) and next_char != "#" and prev_char != "#":
            matches.append((ii, ii + number))
    return matches


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day12")
    part1(input)
