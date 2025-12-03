package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day3 = `987654321111111
811111111111119
234234234234278
818181911112111`

func TestDay3Part1(t *testing.T) {
	assert.Equal(t, "357", Day3Part1(example_day3))
}

func Test_get_max_joltage(t *testing.T) {
	testcases := []struct {
		batteries string
		expected  string
	}{
		{"987654321111111", "98"},
		{"811111111111119", "89"},
		{"234234234234278", "78"},
		{"818181911112111", "92"},
	}
	for _, tc := range testcases {
		t.Run(tc.batteries, func(t *testing.T) {
			assert.Equal(t, tc.expected, get_max_joltage(tc.batteries))
		})
	}
}

func Test_get_max_joltage_and_rest(t *testing.T) {
	testcases := []struct {
		input         string
		max_limit     int
		expected_max  int
		expected_rest string
	}{
		{"811111111111119", 9, 9, ""},
		{"811111111111119", 8, 8, "11111111111119"},
		{"811111111111119", 1, 1, "1111111111119"},
		{"5432", 9, 5, "432"},
	}
	for _, tc := range testcases {
		t.Run(tc.input, func(t *testing.T) {
			max, rest := get_max_joltage_and_rest(tc.input, tc.max_limit)
			assert.Equal(t, tc.expected_max, max)
			assert.Equal(t, tc.expected_rest, rest)
		})
	}
}
