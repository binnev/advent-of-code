import numpy
import utils


def init(raw: str):
    return raw.splitlines()


mapping = {
    "{": "}",
    "(": ")",
    "<": ">",
    "[": "]",
}
reverse_mapping = {v: k for k, v in mapping.items()}
openers = mapping.keys()
closers = mapping.values()

illegal_chars = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

completion_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def check_line1(line):
    stack = []
    for char in line:
        if char in openers:
            stack.append(char)
        else:
            expected_opener = reverse_mapping[char]
            if stack[-1] != expected_opener:
                return illegal_chars[char]
            else:
                stack.pop()
    if len(stack) == 0:
        return 0
    else:
        return 0


def check_line2(line):
    stack = []
    for char in line:
        if char in openers:
            stack.append(char)
        else:
            expected_opener = reverse_mapping[char]
            if stack[-1] != expected_opener:
                return 0
            else:
                stack.pop()
    if len(stack) == 0:
        return 0
    else:
        remaining_chars = []
        while stack:
            char = stack.pop()
            remaining_chars.append(mapping[char])
        return remaining_chars


@utils.profile
def part1(raw: str):
    input = init(raw)
    score = 0
    for line in input:
        score += check_line1(line)
    return score


def calculate_score(chars):
    score = 0
    for char in chars:
        char_score = completion_scores[char]
        score *= 5
        score += char_score
    return score


@utils.profile
def part2(raw: str):
    input = init(raw)
    scores = []
    for line in input:
        remaining_chars = check_line2(line)
        if not remaining_chars:
            continue
        s = calculate_score(remaining_chars)
        scores.append(s)
    return int(numpy.median(scores))


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day10")
    assert part1(raw) == 168417
    assert part2(raw) == 2802519786
