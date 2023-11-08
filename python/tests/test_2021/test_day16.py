import pytest
from puzzles.y2021.day16 import parse, hex_to_bin


@pytest.mark.parametrize(
    "hex_string, expected_value",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_parse(hex_string, expected_value):
    values, remainder = parse(hex_to_bin(hex_string))
    assert values[0] == expected_value


@pytest.mark.parametrize(
    "hex_string, expected_value",
    [
        ("0", "0000"),
        ("0", "0000"),
        ("1", "0001"),
        ("2", "0010"),
        ("3", "0011"),
        ("4", "0100"),
        ("5", "0101"),
        ("6", "0110"),
        ("7", "0111"),
        ("8", "1000"),
        ("9", "1001"),
        ("A", "1010"),
        ("B", "1011"),
        ("C", "1100"),
        ("D", "1101"),
        ("E", "1110"),
        ("F", "1111"),
        ("C200B40A82", "1100001000000000101101000000101010000010"),
        ("04005AC33890", "000001000000000001011010110000110011100010010000"),
        ("880086C3E88112", "10001000000000001000011011000011111010001000000100010010"),
        ("CE00C43D881120", "11001110000000001100010000111101100010000001000100100000"),
        ("D8005AC2A8F0", "110110000000000001011010110000101010100011110000"),
        ("F600BC2D8F", "1111011000000000101111000010110110001111"),
        ("9C005AC2F8F0", "100111000000000001011010110000101111100011110000"),
        (
            "9C0141080250320F1802104A08",
            "10011100000000010100000100001000000000100101000000110010000011110001100000000010000100000100101000001000",
        ),
    ],
)
def test_hex_to_bin(hex_string, expected_value):
    value = hex_to_bin(hex_string)
    assert value == expected_value
