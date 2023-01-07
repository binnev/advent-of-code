package _2022

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestReadList(t *testing.T) {
	type TestCase struct {
		description string
		inputStr    string
		inputStart  int
		expectedStr string
		expectedInt int
	}
	testCases := []TestCase{
		{
			description: "empty list",
			inputStr:    "[]",
			inputStart:  0,
			expectedStr: "[]",
			expectedInt: 2,
		},
		{
			description: "flat list",
			inputStr:    "[1,2,3]",
			inputStart:  0,
			expectedStr: "[1,2,3]",
			expectedInt: 7,
		},
		{
			description: "nested list",
			inputStr:    "[1,[2,3]]",
			inputStart:  3,
			expectedStr: "[2,3]",
			expectedInt: 8,
		},
		{
			description: "outer list including nested list",
			inputStr:    "[1,[2,3]]",
			inputStart:  0,
			expectedStr: "[1,[2,3]]",
			expectedInt: 9,
		},
	}
	for _, tc := range testCases {
		t.Run(tc.description, func(t *testing.T) {
			resultStr, resultInt := readList(tc.inputStr, tc.inputStart)
			assert.Equal(t, resultStr, tc.expectedStr)
			assert.Equal(t, resultInt, tc.expectedInt)
		})
	}
}

func TestReadNumber(t *testing.T) {
	type TestCase struct {
		description string
		inputStr    string
		inputStart  int
		expectedStr string
		expectedInt int
	}
	testCases := []TestCase{
		{
			description: "single number",
			inputStr:    "1",
			inputStart:  0,
			expectedStr: "1",
			expectedInt: 1,
		},
		{
			description: "double digit number",
			inputStr:    "10",
			inputStart:  0,
			expectedStr: "10",
			expectedInt: 2,
		},
		{
			description: "single number in list",
			inputStr:    "[1,]",
			inputStart:  1,
			expectedStr: "1",
			expectedInt: 2,
		},
		{
			description: "double digit number in list",
			inputStr:    "[10,]",
			inputStart:  1,
			expectedStr: "10",
			expectedInt: 3,
		},
		{
			description: "double digit number in middle of list",
			inputStr:    "[[10,1],69,[420,[666]]]",
			inputStart:  8,
			expectedStr: "69",
			expectedInt: 10,
		},
	}
	for _, tc := range testCases {
		t.Run(tc.description, func(t *testing.T) {
			resultStr, resultInt := readNumber(tc.inputStr, tc.inputStart)
			assert.Equal(t, resultStr, tc.expectedStr)
			assert.Equal(t, resultInt, tc.expectedInt)
		})
	}
}

func TestReadValues(t *testing.T) {
	type TestCase struct {
		description string
		input       string
		expected    []string
	}
	testCases := []TestCase{
		{
			description: "empty list",
			input:       "[]",
			expected:    []string{},
		},
		{
			description: "single number",
			input:       "[1]",
			expected:    []string{"1"},
		},
		{
			description: "flat list",
			input:       "[1,2,3]",
			expected:    []string{"1", "2", "3"},
		},
		{
			description: "nested lists",
			input:       "[1,[2,3],4]",
			expected:    []string{"1", "[2,3]", "4"},
		},
		{
			description: "complex",
			input:       "[[10,1],69,[420,[666]]]",
			expected:    []string{"[10,1]", "69", "[420,[666]]"},
		},
	}
	for _, tc := range testCases {
		t.Run(tc.description, func(t *testing.T) {
			result := readValues(tc.input)
			assert.Equal(t, result, tc.expected)
		})
	}
}

func TestArePacketsOrdered(t *testing.T) {
	type TestCase struct {
		description string
		left        string
		right       string
		expected    int
	}
	testCases := []TestCase{
		{
			description: "both empty strings",
			left:        "",
			right:       "",
			expected:    UNKNOWN,
		},
		{
			description: "identical integers",
			left:        "69",
			right:       "69",
			expected:    UNKNOWN,
		},
		{
			description: "identical flat lists",
			left:        "[69,420]",
			right:       "[69,420]",
			expected:    UNKNOWN,
		},
		{
			description: "flat lists; ordered",
			left:        "[69,420]",
			right:       "[420,69]",
			expected:    ORDERED,
		},
		{
			description: "flat lists; unordered",
			left:        "[420,69]",
			right:       "[69,420]",
			expected:    UNORDERED,
		},
		{
			description: "nested empty lists; ordered",
			left:        "[[]]",
			right:       "[[[]]]",
			expected:    ORDERED,
		},
		{
			description: "nested empty lists; unordered",
			left:        "[[[[]]]]",
			right:       "[[[]]]",
			expected:    UNORDERED,
		},
		{
			description: "example pair 1",
			left:        "[1,1,3,1,1]",
			right:       "[1,1,5,1,1]",
			expected:    ORDERED,
		},
		{
			description: "example pair 2",
			left:        "[[1],[2,3,4]]",
			right:       "[[1],4]",
			expected:    ORDERED,
		},
		{
			description: "example pair 3",
			left:        "[9]",
			right:       "[[8,7,6]]",
			expected:    UNORDERED,
		},
		{
			description: "example pair 4",
			left:        "[[4,4],4,4]",
			right:       "[[4,4],4,4,4]",
			expected:    ORDERED,
		},
		{
			description: "example pair 5",
			left:        "[7,7,7,7]",
			right:       "[7,7,7]",
			expected:    UNORDERED,
		},
		{
			description: "example pair 6",
			left:        "[]",
			right:       "[3]",
			expected:    ORDERED,
		},
		{
			description: "example pair 7",
			left:        "[[[]]]",
			right:       "[[]]",
			expected:    UNORDERED,
		},
		{
			description: "example pair 8",
			left:        "[1,[2,[3,[4,[5,6,7]]]],8,9]",
			right:       "[1,[2,[3,[4,[5,6,0]]]],8,9]",
			expected:    UNORDERED,
		},
	}
	for _, tc := range testCases {
		t.Run(tc.description, func(t *testing.T) {
			result := arePacketsOrdered(tc.left, tc.right)
			assert.Equal(t, result, tc.expected)
		})
	}
}
