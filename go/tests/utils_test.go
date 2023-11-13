package tests

import (
	"advent/utils"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMaxIntHappy(t *testing.T) {
	assert.Equal(t, utils.Max([]int{1, 2, 3}), 3)
	assert.Equal(t, utils.Max([]int{-1, -2, -3}), -1)
	assert.Equal(t, utils.Max([]int{-1, 2, -3}), 2)
	assert.Equal(t, utils.Max([]int{0}), 0)
	assert.Equal(t, utils.Max([]int{1, 0, 0, 0, -1}), 1)
	assert.Equal(t, utils.Max([]int{0, 0, 1000, 0, -1000}), 1000)
}

func TestMaxFloatHappy(t *testing.T) {
	assert.Equal(t, utils.Max([]float64{4, 5, 7}), 7.0)
	assert.Equal(t, utils.Max([]float64{4.0, 5.0, 7.0}), 7.0)
	assert.Equal(t, utils.Max([]float64{-4.0, -5.0, -7.0}), -4.0)
	assert.Equal(t, utils.Max([]float64{6.9, 4.20, -666.666}), 6.9)
	assert.Equal(t, utils.Max([]float64{0.0}), 0.0)
}

func TestMaxEmptyArray(t *testing.T) {
	assert.Panics(t, func() { utils.Max([]int{}) }, "Max of empty array should panic")
	assert.Panics(t, func() { utils.Max([]float64{}) }, "Max of empty array should panic")
}

func TestMinIntHappy(t *testing.T) {
	assert.Equal(t, utils.Min([]int{1, 2, 3}), 1)
	assert.Equal(t, utils.Min([]int{-1, -2, -3}), -3)
	assert.Equal(t, utils.Min([]int{-1, 2, -3}), -3)
	assert.Equal(t, utils.Min([]int{0}), 0)
	assert.Equal(t, utils.Min([]int{1, 0, 0, 0, -1}), -1)
	assert.Equal(t, utils.Min([]int{0, 0, 1000, 0, -1000}), -1000)
}

func TestMinFloatHappy(t *testing.T) {
	assert.Equal(t, utils.Min([]float64{4, 5, 7}), 4.0)
	assert.Equal(t, utils.Min([]float64{4.0, 5.0, 7.0}), 4.0)
	assert.Equal(t, utils.Min([]float64{-4.0, -5.0, -7.0}), -7.0)
	assert.Equal(t, utils.Min([]float64{6.9, 4.20, -666.666}), -666.666)
	assert.Equal(t, utils.Min([]float64{0.0}), 0.0)
}

func TestMinEmptyArray(t *testing.T) {
	assert.Panics(t, func() { utils.Min([]int{}) }, "Min of empty array should panic")
	assert.Panics(t, func() { utils.Min([]float64{}) }, "Min of empty array should panic")
}

func TestSumIntHappy(t *testing.T) {
	assert.Equal(t, utils.Sum([]int{1, 2, 3}), 6)
	assert.Equal(t, utils.Sum([]int{1}), 1)
	assert.Equal(t, utils.Sum([]int{5}), 5)
	assert.Equal(t, utils.Sum([]int{-5}), -5)
	assert.Equal(t, utils.Sum([]int{5, -5}), 0)
	assert.Equal(t, utils.Sum([]int{0, 0}), 0)
	assert.Equal(t, utils.Sum([]int{}), 0)
}

func TestSumFloatHappy(t *testing.T) {
	assert.Equal(t, utils.Sum([]float64{1, 2, 3}), 6.0)
	assert.Equal(t, utils.Sum([]float64{1}), 1.0)
	assert.Equal(t, utils.Sum([]float64{5}), 5.0)
	assert.Equal(t, utils.Sum([]float64{-5}), -5.0)
	assert.Equal(t, utils.Sum([]float64{5, -5}), 0.0)
	assert.Equal(t, utils.Sum([]float64{0.0}), 0.0)
	assert.Equal(t, utils.Sum([]float64{}), 0.0)
}

func TestReverse(t *testing.T) {
	type TestCase struct {
		description string
		input       []string
		expected    []string
	}
	cases := []TestCase{
		{
			description: "empty",
			input:       []string{},
			expected:    []string{},
		},
		{
			description: "single entry",
			input:       []string{"a"},
			expected:    []string{"a"},
		},
		{
			description: "populated odd",
			input:       []string{"a", "b", "c"},
			expected:    []string{"c", "b", "a"},
		},
		{
			description: "populated even",
			input:       []string{"...", "aaa", "...", "bbb"},
			expected:    []string{"bbb", "...", "aaa", "..."},
		},
		{
			description: "short",
			input:       []string{"A", ".", "B"},
			expected:    []string{"B", ".", "A"},
		},
		{
			description: "medium",
			input:       []string{"A", ".", ".", "B"},
			expected:    []string{"B", ".", ".", "A"},
		},
		{
			description: "long",
			input:       []string{"A", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=9",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=10",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=11",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=12",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
	}
	for _, tc := range cases {
		t.Run(tc.description, func(t *testing.T) {
			reversed := make([]string, len(tc.input))
			for ii, value := range tc.input {
				reversed[ii] = value
			}
			utils.Reverse(reversed)
			assert.Equal(t, tc.expected, reversed)
		})
	}
}
