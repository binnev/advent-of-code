package _2023

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_regexMagic(t *testing.T) {
	type TestCase struct {
		s        string
		expected []string
	}
	cases := []TestCase{
		{"eightone", []string{"eight", "one"}},
		{"twone", []string{"two", "one"}},
		{"nineight", []string{"nine", "eight"}},
		{"nine9", []string{"nine", "9"}},
	}
	for _, tc := range cases {
		t.Run(tc.s, func(t *testing.T) {
			result := regexMagic(tc.s)
			assert.Equal(t, tc.expected, result)
		})
	}
}
