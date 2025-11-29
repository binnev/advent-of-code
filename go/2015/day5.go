package _2015

import (
	"fmt"
	"strings"
)

func Day5Part1(input string) string {
	count := 0
	for line := range strings.Lines(input) {
		if is_string_nice(line) {
			count++
		}
	}
	return fmt.Sprint(count)
}
func Day5Part2(input string) string {
	return ""
}

func is_string_nice(input string) bool {
	illegal := []string{"ab", "cd", "pq", "xy"}
	return contains_3_vowels(input) && contains_one_double_letter(input) && !contains_illegal_strings(input, illegal)
}

func contains_3_vowels(input string) bool {
	vowels := "aeiou"
	count := 0
	for _, ch := range input {
		if strings.ContainsRune(vowels, ch) {
			count++
		}
		if count >= 3 {
			return true
		}
	}
	return false
}

func contains_one_double_letter(input string) bool {
	left := input[0]
	for ii := 1; ii < len(input); ii++ {
		right := input[ii]
		if left == right {
			return true
		}
		left = right
	}
	return false
}

func contains_illegal_strings(input string, illegal []string) bool {
	for _, substr := range illegal {
		if strings.Contains(input, substr) {
			return true
		}
	}
	return false
}
