import utils

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


def parse_input(raw: str) -> list[list[int, int]]:
    lines = raw.split("\n")
    moves = [[mapping[l] for l in line.split()] for line in lines]
    return moves


def left_wins(a: int, b: int) -> bool | None:
    """
    return True if left wins; False if right wins; None if draw
    """
    if a == b:
        return None  # draw

    return (a, b) in [
        (PAPER, ROCK),  # paper beats rock
        (SCISSORS, PAPER),  # rock beats scissors
        (ROCK, SCISSORS),  # scissors beats paper
    ]


def score_round(opponent, you) -> int:
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
def part1(raw: str) -> int:
    """
    The winner of the whole tournament is the player with the highest score. Your total score is
    the sum of your scores for each round.
    """
    rounds = parse_input(raw)
    score = 0
    for opponent, you in rounds:
        score += score_round(opponent=opponent, you=you)
    return score


def select_move(opponent, objective) -> int:
    if objective == DRAW:
        return opponent  # do same move
    elif objective == WIN:
        return {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}[opponent]
    elif objective == LOSE:
        return {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}[opponent]
    else:
        raise Exception("Panic!")


@utils.profile
def part2(raw: str) -> int:
    rounds = parse_input(raw)
    score = 0
    for opponent, objective in rounds:
        you = select_move(opponent=opponent, objective=objective)
        score += score_round(opponent, you)
    return score


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day2")
    assert part1(raw) == 14264
    assert part2(raw) == 12382
