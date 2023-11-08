import numpy

import utils

LITERAL = 4
SUM = 0
PRODUCT = 1
MIN = 2
MAX = 3
GREATER = 5
LESSER = 6
EQUAL = 7


def hex_to_bin(hex_string):
    return "".join(bin(int(char, base=16)).replace("0b", "").rjust(4, "0") for char in hex_string)


def split(string, index):
    return string[:index], string[index:]


def parse(string, num_packets=None) -> (list, str):
    VERSIONS = []
    results = []
    ii = 1
    while "1" in string:
        version, string = split(string, 3)
        version = int(version, 2)
        VERSIONS.append(version)
        typ, string = split(string, 3)
        typ = int(typ, 2)
        if typ == LITERAL:
            value, string = parse_literal(string)
            results.append(value)
        else:
            value, string = parse_operator(string, typ)
            results.append(value)

        if ii == num_packets:
            break
        ii += 1
    return results, string


def parse_literal(string):
    keep_reading = True
    content = ""
    while keep_reading:
        keep_reading, string = split(string, 1)
        keep_reading = bool(int(keep_reading))
        chunk, string = split(string, 4)
        content += chunk
    return int(content, 2), string


def parse_operator(string, typ):
    length_type, string = split(string, 1)
    if length_type == "0":
        # 15 bit number representing the number of BITS in the sub-packets to follow
        length_in_bits, string = split(string, 15)
        length = int(length_in_bits, 2)
        chunk, string = split(string, length)
        values, _ = parse(chunk)

    elif length_type == "1":
        # 11-bit number representing the number of sub-packets
        num_sub_packets, string = split(string, 11)
        num_sub_packets = int(num_sub_packets, 2)
        values, string = parse(string, num_packets=num_sub_packets)

    mapping = {
        SUM: sum,
        PRODUCT: numpy.product,
        MIN: min,
        MAX: max,
        GREATER: lambda args: int(args[0] > args[1]),
        LESSER: lambda args: int(args[0] < args[1]),
        EQUAL: lambda args: int(args[0] == args[1]),
    }
    operator = mapping[typ]
    return operator(values), string


@utils.profile
def part1(raw: str):
    hex_bin_mapping = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    def hex_to_bin(hex_string):
        return "".join(hex_bin_mapping[char] for char in hex_string)

    def split(string, index):
        return string[:index], string[index:]

    VERSIONS = []

    def parse(string, num_packets=None, len_packets=None) -> (list, str):
        if num_packets and len_packets:
            raise Exception("pick one")

        if len_packets:
            string, remainder = split(string, len_packets)
            return parse(string), remainder

        results = []
        ii = 0
        while "1" in string:
            version, string = split(string, 3)
            version = int(version, 2)
            VERSIONS.append(version)
            typ, string = split(string, 3)
            typ = int(typ, 2)
            if typ == 4:
                value, string = parse_literal(string)
                results.append((value, version, typ))
            else:
                values, string = parse_operator(string)
                results.extend(values)

            if num_packets and ii == num_packets:
                break
            ii += 1
        return results, string

    def parse_literal(string):
        keep_reading = True
        content = ""
        while keep_reading:
            keep_reading, string = split(string, 1)
            keep_reading = bool(int(keep_reading))
            chunk, string = split(string, 4)
            content += chunk
        return int(content, 2), string

    def parse_operator(string):
        length_type, string = split(string, 1)
        if length_type == "0":
            # 15 bit number representing the number of BITS in the sub-packets to follow
            length_in_bits, string = split(string, 15)
            length = int(length_in_bits, 2)
            return parse(string, len_packets=length)
            # chunk, string = split(string, length)
            # values, string = parse(chunk)
            # return values, string

        elif length_type == "1":
            # 11-bit number representing the number of sub-packets
            num_sub_packets, string = split(string, 11)
            num_sub_packets = int(num_sub_packets, 2)
            return parse(string, num_packets=num_sub_packets)
        return None, string

    for hex_string in [
        # "D2FE28",
        # "38006F45291200",
        # "EE00D40C823060",
        # "A0016C880162017C3686B18A3D4780",
        raw
    ]:
        print(f"{hex_string}: ", end="")
        print(parse(hex_to_bin(hex_string)))
        print(VERSIONS)
        return sum(VERSIONS)


@utils.profile
def part2(raw: str):
    values, remainder = parse(hex_to_bin(raw))
    return values[0]


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day16")
    assert part1(raw) == 934
    assert part2(raw) == 912901337844
