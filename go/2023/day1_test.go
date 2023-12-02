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

var example1 = `1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet`

var example2 = `two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen`

func TestPart1(t *testing.T) {
	result := Day1Part1(example1)
	expected := "142"
	assert.Equal(t, expected, result)
}

func TestPart2(t *testing.T) {
	result := Day1Part2(example2)
	expected := "281"
	assert.Equal(t, expected, result)
}
