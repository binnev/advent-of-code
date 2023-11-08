import re
from copy import deepcopy
from itertools import cycle, combinations, combinations_with_replacement
import utils


def init(raw_string):
    return [int(re.findall("\d+", line)[-1]) for line in raw_string.splitlines()]


class DeterministicDie:
    next_result = 1
    times_rolled = 0

    @classmethod
    def roll(cls):
        result = cls.next_result
        cls.times_rolled += 1
        cls.next_result = result + 1 if result + 1 <= 100 else 1
        return result


class Player:
    board = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def __init__(self, player_number, starting_space):
        self.index = starting_space - 1
        self.player_number = player_number
        self.score = 0

    def move(self, spaces):
        self.index = (self.index + spaces) % 10
        self.score += self.position

    @property
    def position(self):
        return self.board[self.index]

    def __repr__(self):
        return f"Player {self.player_number}: position={self.position}, score={self.score}"


@utils.profile
def part1(raw: str):
    player1, player2 = init(raw)
    player1 = Player(1, player1)
    player2 = Player(2, player2)
    for player in cycle([player1, player2]):
        rolls = [DeterministicDie.roll() for _ in range(3)]
        player.move(sum(rolls))
        if player.score >= 1000:
            break
    min_score = min([p.score for p in (player1, player2)])
    return min_score * DeterministicDie.times_rolled


def we_must_go_deeper(players, active_player: int, spaces_to_move: int):
    players = deepcopy(players)
    player = players[active_player]
    player.move(spaces_to_move)
    if player.score >= 13:
        return {active_player: 1}
    else:
        tree = dict()
        combos = list(combinations_with_replacement([1, 2, 3], r=3))
        for rolls in combos:
            spaces = sum(rolls)
            deeper_branches = we_must_go_deeper(
                players,
                active_player=int(not active_player),
                spaces_to_move=spaces,
            )
            for player, wins in deeper_branches.items():
                tree[player] = tree.get(player, 0) + 1
        return tree


@utils.profile
def part2(raw: str):
    player1, player2 = init(raw)
    player1 = Player(1, player1)
    player2 = Player(2, player2)
    results = we_must_go_deeper(
        [player1, player2],
        active_player=1,
        spaces_to_move=0,
    )
    return results


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day21")
    assert part1(raw) == 1073709
