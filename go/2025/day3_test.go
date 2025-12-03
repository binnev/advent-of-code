package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day3 = `987654321111111
811111111111119
234234234234278
818181911112111`

const example_day3_part2 = `987654321111111
811111111111119
234234234234278
818181911112111`

func TestDay3Part1(t *testing.T) {
	assert.Equal(t, "357", Day3Part1(example_day3))
}

func TestDay3Part2(t *testing.T) {
	assert.Equal(t, "3121910778619", Day3Part2(example_day3_part2))
}

func Test_get_max_joltage(t *testing.T) {
	testcases := []struct {
		input    string
		n        int
		expected string
	}{
		// Part 1 examples
		{"987654321111111", 2, "98"},
		{"811111111111119", 2, "89"},
		{"234234234234278", 2, "78"},
		{"818181911112111", 2, "92"},
		// Part 2 examples
		{"987654321111111", 12, "987654321111"},
		{"811111111111119", 12, "811111111119"},
		{"234234234234278", 12, "434234234278"},
		{"818181911112111", 12, "888911112111"},
		// My examples
		{"0123456789", 1, "9"},
		{"0123456789", 2, "89"},
		{"0123456789", 3, "789"},
		{"0123456789", 200, "0123456789"},
		{"abdef", 1, "f"}, // useless, but cool side effect
		{"abdef", 2, "ef"},
	}
	for _, tc := range testcases {
		t.Run(tc.input, func(t *testing.T) {
			assert.Equal(t, tc.expected, get_max_joltage(tc.input, tc.n))
		})
	}
}
