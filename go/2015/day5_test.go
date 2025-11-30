package _2015

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_Day5Part2(t *testing.T) {

	// qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj)
	// and a letter that repeats with exactly one letter between them (zxz).
	input := "qjhvhtzxzqqjkmpb"
	assert.Equal(t, true, contains_palindrome(input))
	assert.Equal(t, true, contains_repeated_pair(input))
	assert.Equal(t, true, is_string_nice2(input))

	// xxyxx is nice because it has a pair that appears twice and a letter that
	// repeats with one between, even though the letters used by each rule
	// overlap.
	input = "xxyxx"
	assert.Equal(t, true, contains_palindrome(input))
	assert.Equal(t, true, contains_repeated_pair(input))
	assert.Equal(t, true, is_string_nice2(input))

	// uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with
	// a single letter between them.
	input = "uurcxstgmygtbstg"
	assert.Equal(t, false, contains_palindrome(input))
	assert.Equal(t, true, contains_repeated_pair(input))
	assert.Equal(t, false, is_string_nice2(input))

	// ieodomkazucvgmuy is naughty because it has a repeating letter with one
	// between (odo), but no pair that appears twice.
	input = "ieodomkazucvgmuy"
	assert.Equal(t, true, contains_palindrome(input))
	assert.Equal(t, false, contains_repeated_pair(input))
	assert.Equal(t, false, is_string_nice2(input))
}

func Test_contains_repeated_pair(t *testing.T) {
	assert.Equal(t, false, contains_repeated_pair("xxx"))
	assert.Equal(t, false, contains_repeated_pair("xyx"))
	assert.Equal(t, false, contains_repeated_pair("xyyx"))
	assert.Equal(t, false, contains_repeated_pair("xyyyx"))

	assert.Equal(t, true, contains_repeated_pair("xxyxx"))
	assert.Equal(t, true, contains_repeated_pair("xxxx"))
	assert.Equal(t, true, contains_repeated_pair("xyxy"))
}

func Test_pair_overlaps(t *testing.T) {
	assert.Equal(t, true, pair_overlaps(1, 2))
	assert.Equal(t, true, pair_overlaps(2, 1))
	assert.Equal(t, true, pair_overlaps(0, 1))
	assert.Equal(t, true, pair_overlaps(1, 0))

	assert.Equal(t, false, pair_overlaps(0, 2))
	assert.Equal(t, false, pair_overlaps(2, 0))
	assert.Equal(t, false, pair_overlaps(1, 3))
	assert.Equal(t, false, pair_overlaps(3, 1))
}
