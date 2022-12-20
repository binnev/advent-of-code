import numpy

from python import utils

example = """1
2
-3
3
-2
0
4"""


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
    encryption_key = 811589153
    input = utils.load_puzzle_input("2022/day20")
    original_ordering = tuple(map(int, input.splitlines()))
    original_ordering = tuple(n * encryption_key for n in original_ordering)
    unique = tuple((salt, num) for salt, num in enumerate(original_ordering))
    assert len(set(unique)) == len(original_ordering)
    length = len(unique)
    mutable = list(unique)

    for _ in range(10):
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


if __name__ == "__main__":
    assert part1() == 14888
    assert part2() == 3760092545849
