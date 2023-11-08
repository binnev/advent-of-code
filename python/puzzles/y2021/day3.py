import utils


def more_1s(input: list[str]) -> bool:
    return input.count("1") >= len(input) / 2


def most_common_element(input: list[str]):
    return "1" if more_1s(input) else "0"


def least_common_element(input: list[str]):
    return "0" if more_1s(input) else "1"


@utils.profile
def part1(raw: str):
    input = raw.splitlines()
    gamma_rate = "".join(map(most_common_element, zip(*input)))
    epsilon_rate = "".join(map(least_common_element, zip(*input)))
    epsilon_rate = int(epsilon_rate, 2)
    gamma_rate = int(gamma_rate, 2)
    return epsilon_rate * gamma_rate


def search(numbers, position, bit_criterion):
    bits = list(zip(*numbers))[position]
    target_value = bit_criterion(bits)
    numbers = [n for n in numbers if n[position] == target_value]
    if len(numbers) == 1:
        return numbers[0]
    else:
        return search(numbers, position + 1, bit_criterion)


@utils.profile
def part2(raw: str):
    input = raw.splitlines()
    oxygen_rating = int(search(input, position=0, bit_criterion=most_common_element), 2)
    co2_rating = int(search(input, position=0, bit_criterion=least_common_element), 2)
    return oxygen_rating * co2_rating


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day3")
    assert part1(raw) == 3549854
    assert part2(raw) == 3765399
