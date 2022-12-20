from python import utils
import numpy
import string

example = """1
2
-3
3
-2
0
4"""


def shift_one(mutable: list[int], item, direction: int, length: int) -> list[int]:
    index = mutable.index(item)
    new_index = index + direction
    if new_index == 0:
        new_index = length
    elif new_index >= length:
        new_index = new_index % (length - 1)
    mutable.pop(index)
    mutable.insert(new_index, item)
    return mutable


def shift_naive(mutable: list[int], item, move: int, length: int) -> list[int]:
    """
    Do it manually 1 step at a time
    """
    direction = numpy.sign(move)
    amount = abs(move)
    for _ in range(amount):
        mutable = shift_one(mutable, item, direction, length)

    return mutable


def shift_right(index: int, move: int, length: int) -> int:
    new_index = index + move
    new_index = new_index % (length - 1)
    # if new_index == 0:
    #     new_index = length - 1
    return new_index


def move_from(index: int, new_index: int, mutable: list):
    item = mutable[index]
    mutable[index] = None
    mutable.insert(new_index, item)
    mutable.pop(mutable.index(None))


def shift_number(mutable: list[int], item, move: int, length: int) -> list[int]:
    """
    Apparently moving to position 0 is not allowed. Instead we put the number on the end.
    """
    amount = abs(move)
    direction = numpy.sign(move)
    complete_cycle = length - 1
    amount = amount % complete_cycle
    new_move = amount * direction
    index = mutable.index(item)
    if direction > 0:
        new_index = (index + new_move) % length + 1
    else:
        new_index = (length + new_move + index) % length
    if new_index == index:
        return mutable  # no move required
    if new_index == 0:
        new_index = length  # why
    mutable[index] = None
    mutable.insert(new_index, item)
    mutable.pop(mutable.index(None))
    return mutable


@utils.profile
def part1():
    # input = example
    input = utils.load_puzzle_input("2022/day20")
    original_ordering = tuple(map(int, input.splitlines()))
    unique = tuple((salt, num) for salt, num in enumerate(original_ordering))
    assert len(set(unique)) == len(original_ordering)
    length = len(unique)
    mutable = list(unique)

    for item in unique:
        move = item[1]
        mutable = shift_number(mutable, item, move=move, length=length)

    zero_index = next(ii for ii, (_, value) in enumerate(mutable) if value == 0)
    result = 0
    for interval in 1000, 2000, 3000:
        index = (zero_index + interval) % length
        _, value = mutable[index]
        result += value
    return result


@utils.profile
def part2():
    ...


if __name__ == "__main__":
    assert part1() == 14888
    part2()
