package _2025

import (
	"advent/utils"
	"fmt"
	"strconv"
	"strings"
)

func Day2Part1(input string) string {
	total := 0
	id_ranges := parse_id_ranges(input)
	for _, id_range := range id_ranges {
		invalid_ids := get_invalid_ids(id_range[0], id_range[1])
		total += utils.Sum(invalid_ids)
	}
	return fmt.Sprint(total)
}

// Now, an ID is invalid if it is made only of some sequence of digits repeated
// at least twice. So, 12341234 (1234 two times), 123123123 (123 three times),
// 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.
func Day2Part2(input string) string {
	total := 0
	id_ranges := parse_id_ranges(input)
	for _, id_range := range id_ranges {
		start, end := id_range[0], id_range[1]
		for id := start; id <= end; id++ {
			_, repeats := get_repeating_parts(fmt.Sprint(id))
			if repeats > 1 {
				total += id
			}
		}
	}
	return fmt.Sprint(total)
}

func parse_id_ranges(input string) [][2]int {
	parts := strings.Split(input, ",")
	return utils.Map(parse_id_range, parts)
}
func parse_id_range(input string) [2]int {
	parts := strings.Split(input, "-")
	left, _ := strconv.Atoi(parts[0])
	right, _ := strconv.Atoi(parts[1])
	return [2]int{left, right}
}

// Since the young Elf was just doing silly patterns, you can find the invalid
// IDs by looking for any ID which is made only of some sequence of digits
// repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice)
// would all be invalid IDs.
func is_id_valid(id string) bool {
	length := len(id)

	// odd-length ids are valid by default because they can't be a pattern
	// repeated twice
	if length%2 != 0 {
		return true
	}

	middle := len(id) / 2
	left := id[:middle]
	right := id[middle:]
	return left != right
}

// Find the repeating components that comprise the input string.
// Return the component, and the number of times it repeats.
// E.g. input: "111" -> "1", 3
// E.g. input: "118118" -> "118", 2
// E.g. input: "123", -> "123", 1 (no repeating parts)
func get_repeating_parts(id string) (string, int) {
	start := 0
	middle := len(id) / 2
	for end := 1; end <= middle; end++ {
		part := id[start:end]
		repeats := get_repeats(id, part)
		if repeats > 0 {
			return part, repeats
		}
	}
	return id, 1
}

// If we can construct `input` by repeating `part`, return the number of repeats
// required. If not, return 0.
func get_repeats(input string, part string) int {
	// If part doesn't evenly fit into input
	if len(input)%len(part) != 0 {
		return 0
	}

	repeats := len(input) / len(part)
	if strings.Repeat(part, repeats) == input {
		return repeats
	}
	return 0
}

func get_invalid_ids(start, end int) []int {
	invalid := []int{}
	for id := start; id <= end; id++ {
		if !is_id_valid(strconv.Itoa(id)) {
			invalid = append(invalid, id)
		}
	}
	return invalid
}
