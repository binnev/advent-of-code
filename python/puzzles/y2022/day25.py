import utils

example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

SNAFU_TO_DECIMAL = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2,
}
DECIMAL_TO_SNAFU = {v: k for k, v in SNAFU_TO_DECIMAL.items()}


def snafu_to_decimal(snafu: str) -> int:
    result = 0
    multiplier = 1
    for snafu_digit in reversed(snafu):
        decimal_digit = SNAFU_TO_DECIMAL[snafu_digit]
        result += decimal_digit * multiplier
        multiplier *= 5  # not 10
    return result


def decimal_to_snafu(decimal: str) -> str:
    decimal = int(decimal)
    num_columns = len(str(decimal)) * 2 + 1
    column_values = {5**ii: 0 for ii in range(num_columns)}
    columns = sorted(column_values.keys())
    descending = list(reversed(columns))
    remainder = decimal
    for column in descending:
        value, remainder = divmod(remainder, column)
        column_values[column] = value

    conversions = {
        3: (1, -2),  # 1=
        4: (1, -1),  # 1-
        5: (1, 0),  # 10
        6: (1, 1),  # 11
        7: (1, 2),  # 12
        8: (2, -2),  # 2=
        9: (2, -1),  # 2-
    }
    for column in columns:
        value = column_values[column]
        if value in conversions:
            next_value, new_value = conversions[value]
            column_values[column * 5] = column_values.get(column * 5, 0) + next_value
            column_values[column] = new_value

    output = ""
    for column in columns:
        value = column_values.get(column, 0)
        output = DECIMAL_TO_SNAFU[value] + output

    return output.lstrip("0")


@utils.profile
def part1(raw: str):
    result = 0
    for snafu in raw.splitlines():
        result += snafu_to_decimal(snafu)
    return decimal_to_snafu(result)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day25")
    assert part1(raw) == "20-1-0=-2=-2220=0011"
