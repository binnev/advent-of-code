import operator

import numpy

raw = """0054FEC8C54DC02295D5AE9B243D2F4FEA154493A43E0E60084E61CE802419A95E38958DE4F100B9708300466AB2AB7D80291DA471EB9110010328F820084D5742D2C8E600AC8DF3DBD486C010999B44CCDBD401C9BBCE3FD3DCA624652C400007FC97B113B8C4600A6002A33907E9C83ECB4F709FD51400B3002C4009202E9D00AF260290D400D70038400E7003C400A201B01400B401609C008201115003915002D002525003A6EB49C751ED114C013865800BFCA234E677512952E20040649A26DFA1C90087D600A8803F0CA1AC1F00042A3E41F8D31EE7C8D800FD97E43CCE401A9E802D377B5B751A95BCD3E574124017CF00341353E672A32E2D2356B9EE79088032AF005E7E8F33F47F95EC29AD3018038000864658471280010C8FD1D63C080390E61D44600092645366202933C9FA2F460095006E40008742A8E70F80010F8DF0AA264B331004C52B647D004E6EEF534C8600BCC93E802D38B5311AC7E7B02D804629DD034DFBB1E2D4E2ACBDE9F9FF8ED2F10099DE828803C7C0068E7B9A7D9EE69F263B7D427541200806582E49725CFA64240050A20043E25C148CC600F45C8E717C8010E84506E1F18023600A4D934DC379B9EC96B242402504A027006E200085C6B8D51200010F89913629A805925FBD3322191A1C45A9EACB4733FBC5631A210805315A7E3BC324BCE8573ACF3222600BCD6B3997E7430F004E37CED091401293BEAC2D138402496508873967A840E00E41E99DE6B9D3CCB5E3F9A69802B2368E7558056802E200D4458AF1180010A82B1520DB80212588014C009803B2A3134DD32706009498C600664200F4558630F840188E11EE3B200C292B59124AFF9AE6775ED8BE73D4FEEFFAD4CE7E72FFBB7BB49005FB3BEBFA84140096CD5FEDF048C011B004A5B327F96CC9E653C9060174EA0CF15CA0E4D044F9E4B6258A5065400D9B68"""

"""
1. hex to binary
2. parse headers
3. check for number or operation type
"""

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

LITERAL = 4
SUM = 0
PRODUCT = 1
MIN = 2
MAX = 3
GREATER = 5
LESSER = 6
EQUAL = 7
TYPES = {
    LITERAL: "LITERAL",
    SUM: "SUM",
    PRODUCT: "PRODUCT",
    MIN: "MIN",
    MAX: "MAX",
    GREATER: "GREATER",
    LESSER: "LESSER",
    EQUAL: "EQUAL",
}


def parse(string, num_packets=None, len_packets=None) -> (list, str):
    if num_packets and len_packets:
        raise Exception("pick one")

    if len_packets:
        string, remainder = split(string, len_packets)
        return parse(string)[0], remainder

    results = []
    ii = 0
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


def parse_operator(string, typ):
    length_type, string = split(string, 1)
    if length_type == "0":
        # 15 bit number representing the number of BITS in the sub-packets to follow
        length_in_bits, string = split(string, 15)
        length = int(length_in_bits, 2)
        values, string = parse(string, len_packets=length)

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


for hex_string, expected_value in [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
    # raw
]:
    print(f"{hex_string}: ", end="")
    values, remainder = parse(hex_to_bin(hex_string))
    print(values[0], end="")
    assert values[0] == expected_value
    print(" passed")
