import re

import utils

example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


@utils.profile
def part1(raw: str):
    result = 0
    for line in raw.splitlines():
        digits = re.findall(r"\d", line)
        result += int(digits[0] + digits[-1])
    return result


def regex_magic(s: str) -> list[str]:
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


@utils.profile
def part2(raw: str):
    digit_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    result = 0
    for line in raw.splitlines():
        digit_strings = regex_magic(line)
        digits = [digit_map.get(d, d) for d in digit_strings]
        result += int(digits[0] + digits[-1])
    return result


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2023/day1")
    assert part1(raw) == 55123
    assert part2(raw) == 55260
