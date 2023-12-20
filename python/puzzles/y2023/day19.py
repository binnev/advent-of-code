import re

import utils


@utils.profile
def part1(input: str):
    pass


@utils.profile
def part2(input: str):
    pass


def parse_input(input: str):
    workflows, parts = input.split("\n\n")

    rx = re.compile(
        r"(\w+)"  # workflow name
        r"\{"  # open bracket
        r"("  # start condition group
        r"\w+"  # attribute name
        r"<|>"  # operator (< or >)
        r"[-\d]+"  # threshold value (negative values allowed)
        r":"
        r"\w+"  # next workflow if part passes test
        r"),+"  # multiple conditions ending in comma
        r"(\w+)"  # fallback for if no conditions match part
        r"\}"  # close bracket
    )
    for flow in workflows.splitlines():
        if match := rx.match(flow):
            print(match.groups())


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day19")
    part1(input)
