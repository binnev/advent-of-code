package _2025

import (
	"advent/utils"
	"fmt"
	"strconv"
	"strings"
)

func Day3Part1(input string) string {
	total := 0
	for line := range strings.Lines(input) {
		s := get_max_joltage(strings.TrimSpace(line), 2)
		i, _ := strconv.Atoi(s)
		total += i
	}
	return fmt.Sprint(total)
}
func Day3Part2(input string) string {
	total := 0
	for line := range strings.Lines(input) {
		s := get_max_joltage(strings.TrimSpace(line), 12)
		i, _ := strconv.Atoi(s)
		total += i
	}
	return fmt.Sprint(total)
}

// n is the number of batteries we want to turn on
func get_max_joltage(input string, n int) string {
	descending_chars := utils.Reverse(utils.Sort([]rune(input)))
	out := []rune{}
	search_space := input

	// Look for n batteries
	for remaining := n; remaining > 0; remaining-- {
		// Look for the highest value number first and go downwards
		for _, r := range descending_chars {
			// If the number is not in the string, try the next one
			if !strings.ContainsRune(search_space, r) {
				continue
			}
			pos := strings.IndexRune(search_space, r)
			rest := search_space[pos+1:]
			// If there are not enough remaining characters to turn on n
			// batteries, try the next number
			if len(rest) < remaining-1 {
				continue
			}
			out = append(out, r)
			search_space = rest
			break // start searching from 9 again
		}
	}

	return string(out)
}
