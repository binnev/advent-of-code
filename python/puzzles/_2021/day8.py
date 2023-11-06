import itertools
import utils


raw = utils.load_puzzle_input("2021/day8")


def init():
    data = [list(map(str.split, line.split(" | "))) for line in raw.splitlines()]
    inputs = [input for input, output in data]
    outputs = [output for input, output in data]
    return inputs, outputs


@utils.profile
def part1():
    inputs, outputs = init()
    count = 0
    for output in outputs:
        for digit in output:
            if len(digit) in (2, 3, 4, 7):
                count += 1
    return count


def gen_strings(possible_segments):
    values = list(map(tuple, possible_segments.values()))
    foo = list(itertools.product(*values))
    bar = {"".join(thing) for thing in foo}
    return bar


number_to_segments = {
    1: "BC",
    2: "ABDEG",
    3: "ABCDG",
    4: "BCFG",
    5: "ACDFG",
    6: "ACDEFG",
    7: "ABC",
    8: "ABCDEFG",
    9: "ABCDFG",
    0: "ABCDEF",
}
segments_to_number = {v: k for k, v in number_to_segments.items()}


def deduce_number(wires, mapping):
    possible_numbers = {
        number: segments
        for number, segments in number_to_segments.items()
        if len(segments) == len(wires)
    }
    # this is generating a reverse of mapping. Probably don't need that
    possible_segments = {
        wire: {segment for segment, wires in mapping.items() if wire in wires} for wire in wires
    }
    possible_strings = gen_strings(possible_segments)
    for number, segments in possible_numbers.items():
        if set(segments) in map(set, possible_strings):
            return number
    else:
        print(f"couldn't find match for wires {wires}")


def deduce_mapping(input: [str]):
    """
    My naming of the segments:
     AAAA
    F    B
    F    B
     GGGG
    E    C
    E    C
     DDDD
    """

    unique_lengths = {2: 1, 3: 7, 4: 4, 7: 8}
    mapping = {char: set("abcdefg") for char in "ABCDEFG"}
    unique_wires = [wires for wires in input if len(wires) in unique_lengths]
    mystery_wires = [wires for wires in input if len(wires) not in unique_lengths]

    # use unique length wires to prune mapping
    for wires in unique_wires:
        number = unique_lengths[len(wires)]
        mapping = update_mapping(number, wires, mapping)

    # deduce configuration of mystery wires and update mapping further
    for wires in mystery_wires:
        number = deduce_number(wires, mapping)
        mapping = update_mapping(number, wires, mapping)
        if all(len(value) == 1 for value in mapping.values()):
            break
    # if no unique mapping found
    else:
        raise Exception("Non-unique mapping!")

    mapping = {value.pop(): key for key, value in mapping.items()}
    return mapping


def update_mapping(number: int, wires: str, mapping: dict):
    segments = number_to_segments[number]
    # for each segment associated with this number, take the union of the new wires and the
    # segment's current possibilities. Set that as the possible wires for the segment
    hits = []
    for segment in segments:
        intersection = mapping[segment].intersection(wires)
        hits.append(intersection)
        mapping[segment] = intersection

    # for each intersection found, remove the result from any segments NOT associated with this
    # number
    other_segments = set(mapping.keys()).difference(segments)
    for segment in other_segments:
        for intersection in hits:
            mapping[segment] = mapping[segment].difference(intersection)

    return mapping


def calculate_result(wire_sequence, mapping) -> int:
    result = ""
    for wires in wire_sequence:
        segments = "".join(sorted(mapping[wire] for wire in wires))
        number = segments_to_number[segments]
        result += str(number)
    return int(result)


@utils.profile
def part2():
    inputs, outputs = init()
    total = 0
    for input, output in zip(inputs, outputs):
        mapping = deduce_mapping(input)
        result = calculate_result(output, mapping)
        total += result
    return total


if __name__ == "__main__":
    assert part1() == 303
    assert part2() == 961734
