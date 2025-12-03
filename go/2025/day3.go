package _2025

import (
	"fmt"
	"strconv"
	"strings"
)

func Day3Part1(input string) string {
	total := 0
	for line := range strings.Lines(input) {
		s := get_max_joltage(strings.TrimSpace(line))
		i, _ := strconv.Atoi(s)
		total += i
	}
	return fmt.Sprint(total)
}
func Day3Part2(input string) string {
	return ""
}

func get_max_joltage(input string) string {
	batteries := input
	out := []int{}
	max_limit := 9

	// get first char
	for {
		max, rest := get_max_joltage_and_rest(batteries, max_limit)
		if len(rest) > 0 {
			out = append(out, max)
			batteries = rest
			break
		}
		max_limit -= 1
		if max_limit < 0 {
			panic(fmt.Sprintf("Couldn't find a numeric char in %v", batteries))
		}
	}

	// get second char
	max_limit = 9
	max, _ := get_max_joltage_and_rest(batteries, max_limit)
	out = append(out, max)

	return fmt.Sprintf("%v%v", out[0], out[1])
}

func get_max_joltage_and_rest(input string, max_limit int) (int, string) {
	max := -1
	pos := -1
	for _, r := range input {
		i, _ := strconv.Atoi(string(r))
		if i <= max_limit && i > max {
			max = i
			pos = strings.IndexRune(input, r)
		}
	}
	if pos == -1 {
		panic(fmt.Sprintf("Didn't find any positive integers in %v", input))
	}
	rest := input[pos+1:]
	return max, rest
}
