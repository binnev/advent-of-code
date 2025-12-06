package _2025

import (
	"advent/utils"
	"fmt"
	"strings"
	"unicode"
)

func Day6Part1(input string) string {
	arr := parse_day6(input)
	width := len(arr[0])
	total := 0
	for x := 0; x < width; x++ {
		col := get_col(arr, x)
		total += string_math(col)
	}
	return fmt.Sprint(total)
}
func Day6Part2(input string) string {
	total := 0
	arr := parse_day6_part2(input)
	for _, line := range arr {
		total += string_math(line)
	}
	return fmt.Sprint(total)
}

func string_math(input []string) int {
	// Assume the last entry is the operator
	last := len(input) - 1
	operator := input[last]
	parts := input[:last]
	numbers := utils.Map(utils.ParseInt, parts)
	switch operator {
	case "+":
		return utils.Reduce(func(i1, i2 int) int { return i1 + i2 }, numbers)
	case "*":
		return utils.Reduce(func(i1, i2 int) int { return i1 * i2 }, numbers)
	default:
		panic(fmt.Sprintf("Unrecognised operator %v", operator))
	}
}
func parse_day6(input string) [][]string {
	out := [][]string{}
	for line := range strings.Lines(input) {
		line = strings.TrimSpace(line)
		out = append(out, strings.Fields(line))
	}
	return out
}
func get_col(arr [][]string, x int) []string {
	out := []string{}
	for _, line := range arr {
		out = append(out, line[x])
	}
	return out
}
func parse_day6_part2(input string) [][]string {
	out := [][]string{}
	lines := strings.Split(input, "\n")
	width := len(lines[0])
	current := []string{}
	for x := width - 1; x >= 0; x-- {

		// Construct a 1-wide column
		col := []byte{}
		for _, line := range lines {
			// FIXME: LoadPuzzleInput does TrimSpace, which removes the last few
			// spaces from the operator line...
			var char byte
			if x < len(line) {
				char = line[x]
			} else {
				char = ' '
			}
			col = append(col, char)
		}

		// If every line has a space at this x, skip
		all_space := true
		for _, char := range col {
			if !unicode.IsSpace(rune(char)) {
				all_space = false
				break
			}
		}
		if all_space {
			continue
		}

		end := len(col) - 1
		last := col[end:]
		digits := col[:end]
		number := strings.TrimSpace(string(digits))
		current = append(current, number)

		// If the final char is not space, treat it as the operator and append
		// it to the current sum. Then reset and start parsing the next sum
		if !unicode.IsSpace(rune(last[0])) {
			current = append(current, string(last))
			out = append(out, current)
			current = []string{}
		}
	}
	return out
}
