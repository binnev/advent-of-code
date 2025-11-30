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
	count := 0
	for line := range strings.Lines(input) {
		if is_string_nice2(line) {
			count++
		}
	}
	return fmt.Sprint(count)
}

func is_string_nice(input string) bool {
	illegal := []string{"ab", "cd", "pq", "xy"}
	return contains_3_vowels(input) && contains_one_double_letter(input) && !contains_illegal_strings(input, illegal)
}

func is_string_nice2(input string) bool {
	return contains_repeated_pair(input) && contains_palindrome(input)
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

// It contains a pair of any two letters that appears at least twice in the
// string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like
// aaa (aa, but it overlaps).
func contains_repeated_pair(input string) bool {
	// Construct a map with all the pairs of characters as keys, and the
	// position at which they occured as values. We store the position of the
	// LEFT character. E.g: {"ab": 3}
	pairs := map[string]int{}
	for right := 1; right < len(input); right++ {
		left := right - 1
		pair := input[left : right+1]
		existing, ok := pairs[pair]
		if !ok {
			// new pair -> log location
			pairs[pair] = left
		} else {
			// existing pair
			// If they overlap, ignore it and keep the original one (since that
			// won't overlap with other occurrences)
			if !pair_overlaps(existing, left) {
				return true
			}
		}
	}
	return false
}

func pair_overlaps(left_char_1, left_char_2 int) bool {
	l1 := left_char_1
	r1 := l1 + 1
	l2 := left_char_2
	r2 := l2 + 1
	return (r1 == l2 || r2 == l1)
}

// It contains at least one letter which repeats with exactly one letter between
// them, like xyx, abcdefeghi (efe), or even aaa.
func contains_palindrome(input string) bool {
	for ii := 2; ii < len(input); ii++ {
		one := input[ii-2]
		three := input[ii]
		if one == three {
			return true
		}
	}
	return false
}

type StringChecker interface {
	// Read 1 letter of the string
	read_rune(rune)
	// Returns true if the checker's conditions were satisfied
	result() bool
}

type ContainsIllegalStrings struct {
	illegal []string
	res     bool
}

func (cil *ContainsIllegalStrings) read_rune(r rune) {

}
func (c *ContainsIllegalStrings) result() bool {
	return c.res
}

// This is how you enforce a struct implements an interface in go -.-
var _ StringChecker = (*ContainsIllegalStrings)(nil)
