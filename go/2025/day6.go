package _2025

import (
	"advent/utils"
	"fmt"
	"strings"
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
	return ""
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
