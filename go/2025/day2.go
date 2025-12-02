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
func Day2Part2(input string) string {
	return ""
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

func get_invalid_ids(start, end int) []int {
	invalid := []int{}
	for id := start; id <= end; id++ {
		if !is_id_valid(strconv.Itoa(id)) {
			invalid = append(invalid, id)
		}
	}
	return invalid
}
