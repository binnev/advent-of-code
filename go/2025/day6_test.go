package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day6 = `123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
`

func Test_Day6Part1(t *testing.T) {
	assert.Equal(t, "4277556", Day6Part1(example_day6))
}

func Test_string_math(t *testing.T) {
	testcases := []struct {
		description string
		input       []string
		expected    int
	}{
		{"mult", []string{"123", "45", "6", "*"}, 33210},
		{"add", []string{"328", "64", "98", "+"}, 490},
		{"mult2", []string{"51", "387", "215", "*"}, 4243455},
		{"add2", []string{"64", "23", "314", "+"}, 401},
	}
	for _, tc := range testcases {
		t.Run(tc.description, func(t *testing.T) {
			result := string_math(tc.input)
			assert.Equal(t, tc.expected, result)
		})
	}
}
