from _2021.python import utils

raw = utils.load_puzzle_input("day3")
input = raw.splitlines()


def most_common_element(input: list):
    counts = {item: input.count(item) for item in input}
    highest_count = max(counts.values())
    winners = [key for key, value in counts.items() if value == highest_count]
    return str(max(map(int, winners)))


def least_common_element(input: list):
    counts = {item: input.count(item) for item in input}
    lowest_count = min(counts.values())
    winners = [key for key, value in counts.items() if value == lowest_count]
    return str(min(map(int, winners)))


@utils.profile
def part1():
    gamma_rate = "".join(map(most_common_element, zip(*input)))
    epsilon_rate = "".join(map(least_common_element, zip(*input)))
    epsilon_rate = int(epsilon_rate, 2)
    gamma_rate = int(gamma_rate, 2)
    return epsilon_rate * gamma_rate


def foo(numbers, position, bit_criterion):
    bits = list(zip(*numbers))[position]
    target_value = bit_criterion(bits)
    numbers = [n for n in numbers if n[position] == target_value]
    if len(numbers) == 1:
        return numbers[0]
    else:
        return foo(numbers, position + 1, bit_criterion)


@utils.profile
def part2():
    oxygen_rating = int(foo(input, position=0, bit_criterion=most_common_element), 2)
    co2_rating = int(foo(input, position=0, bit_criterion=least_common_element), 2)
    return oxygen_rating * co2_rating


if __name__ == "__main__":
    assert part1() == 3549854
    assert part2() == 3765399
