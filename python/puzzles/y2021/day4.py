import utils


def parse_board(board):
    return [list(map(int, row.split())) for row in board.splitlines()]


class Board(list):
    @property
    def columns(self):
        return [[row[ii] for row in self] for ii in range(len(self[0]))]

    @property
    def is_complete(self):
        win = ["x"] * 5
        return (win in self) or (win in self.columns)

    @property
    def sum_unmarked(self):
        return sum(number for row in self for number in row if number != "x")

    def mark(self, called_number):
        for row in self:
            for ii, number in enumerate(row):
                if number == called_number:
                    row[ii] = "x"


def init(raw: str):
    numbers, *boards = raw.split("\n\n")
    numbers = list(map(int, numbers.split(",")))
    boards = list(map(Board, map(parse_board, boards)))
    return numbers, boards


@utils.profile
def part1(raw: str):
    numbers, boards = init(raw)
    for called_number in numbers:
        for board in boards:
            board.mark(called_number)
            if board.is_complete:
                return board.sum_unmarked * called_number


@utils.profile
def part2(raw: str):
    numbers, boards = init(raw)
    for called_number in numbers:
        for board in boards:
            board.mark(called_number)

        if len(boards) == 1 and boards[0].is_complete:
            return boards[0].sum_unmarked * called_number

        boards = [b for b in boards if not b.is_complete]


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day4")
    assert part1(raw) == 33348
    assert part2(raw) == 8112
