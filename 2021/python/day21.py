import re
from copy import deepcopy
from itertools import cycle, combinations, combinations_with_replacement

raw = """Player 1 starting position: 9
Player 2 starting position: 3"""

example = """Player 1 starting position: 4
Player 2 starting position: 8"""

# raw = example


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


def part1():
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
    print(f"{active_player=}, {spaces_to_move=}")
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


def part2():
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
    # p1 = part1()
    # print(f"{p1=}")
    # assert p1 == 1073709
    p2 = part2()
    print(f"{p2=}")
