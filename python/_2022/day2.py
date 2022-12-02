from python import utils

raw = """A Y
B X
C Z"""

ROCK = LOSE = 1
PAPER = DRAW = 2
SCISSORS = WIN = 3
mapping = dict(
    A=ROCK,
    B=PAPER,
    C=SCISSORS,
    X=ROCK,
    Y=PAPER,
    Z=SCISSORS,
)


def parse_input():
    input = utils.load_puzzle_input("2022/day2")
    lines = input.split("\n")
    moves = [[mapping[l] for l in line.split()] for line in lines]
    return moves


def left_wins(a: int, b: int) -> int:
    """
    return True if left wins; False if right wins; None if draw
    """
    if a == b:
        return None  # draw

    # paper beats rock
    if (a, b) == (ROCK, PAPER):
        return False
    if (a, b) == (PAPER, ROCK):
        return True

    # rock beats scissors
    if (a, b) == (ROCK, SCISSORS):
        return True
    if (a, b) == (SCISSORS, ROCK):
        return False

    # scissors beats paper
    if (a, b) == (PAPER, SCISSORS):
        return False
    if (a, b) == (SCISSORS, PAPER):
        return True


def score_round(opponent, you):
    """
    The score for a single round is the score for the shape you selected (1 for Rock,
    2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost,
    3 if the round was a draw, and 6 if you won).
    """
    points = you  # shape you selected
    outcome = left_wins(you, opponent)
    if outcome is True:
        points += 6
    elif outcome is False:
        points += 0
    elif outcome is None:
        points += 3
    else:
        raise Exception("panic!")
    return points


@utils.profile
def part1():
    """
    The winner of the whole tournament is the player with the highest score. Your total score is
    the sum of your scores for each round.
    """
    rounds = parse_input()
    score = 0
    for round in rounds:
        opponent, you = round
        score += score_round(opponent=opponent, you=you)
    return score


def select_move(opponent, objective):
    if objective == DRAW:
        return opponent  # do same move
    elif objective == WIN:
        if opponent == ROCK:
            return PAPER
        if opponent == PAPER:
            return SCISSORS
        if opponent == SCISSORS:
            return ROCK
    elif objective == LOSE:
        if opponent == ROCK:
            return SCISSORS
        if opponent == PAPER:
            return ROCK
        if opponent == SCISSORS:
            return PAPER
    else:
        raise Exception("Panic!")


@utils.profile
def part2():
    rounds = parse_input()
    score = 0
    for round in rounds:
        opponent, objective = round
        you = select_move(opponent=opponent, objective=objective)
        score += score_round(opponent, you)
    return score


if __name__ == "__main__":
    # assert part1() == 14264
    part2()
