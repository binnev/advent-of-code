package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day5 = `3-5
10-14
16-20
12-18

1
5
8
11
17
32
`

func Test_Day5Part1(t *testing.T) {
	assert.Equal(t, "3", Day5Part1(example_day5))
}

func Test_Day5Part2(t *testing.T) {
	assert.Equal(t, "14", Day5Part2(example_day5))
}

func Test_range_overlaps(t *testing.T) {
	testcases := []struct {
		description    string
		range1, range2 InclusiveRange
		expected       bool
	}{
		{"no overlap (off by one)", InclusiveRange{0, 1}, InclusiveRange{2, 3}, false},
		{"partial overlap", InclusiveRange{0, 1}, InclusiveRange{1, 3}, true},
		{"exact match", InclusiveRange{0, 1}, InclusiveRange{0, 1}, true},
		{"total overlap", InclusiveRange{0, 3}, InclusiveRange{1, 2}, true},
	}
	for _, tc := range testcases {
		t.Run(tc.description, func(t *testing.T) {
			assert.Equal(t, tc.expected, tc.range1.overlaps(tc.range2))
			assert.Equal(t, tc.expected, tc.range2.overlaps(tc.range1))
		})
	}
}
func Test_merge_ranges(t *testing.T) {
	testcases := []struct {
		description string
		ranges      []InclusiveRange
		expected    []InclusiveRange
	}{
		{
			"No overlapping ranges; output should be unchanged",
			[]InclusiveRange{{0, 1}, {2, 3}},
			[]InclusiveRange{{0, 1}, {2, 3}},
		},
		{
			"2 overlapping ranges merged into 1",
			[]InclusiveRange{{0, 1}, {1, 2}},
			[]InclusiveRange{{0, 2}},
		},
		{
			"3 ranges merged into 2",
			[]InclusiveRange{{0, 1}, {3, 4}, {1, 2}},
			[]InclusiveRange{{0, 2}, {3, 4}},
		},
		{
			"3 overlapping ranges merged into 1",
			[]InclusiveRange{{0, 1}, {2, 3}, {1, 2}},
			[]InclusiveRange{{0, 3}},
		},
		{
			"1 range overlaps 3 other non-overlapping ranges",
			[]InclusiveRange{{0, 1}, {2, 3}, {4, 5}, {0, 6}},
			[]InclusiveRange{{0, 6}},
		},
	}
	for _, tc := range testcases {
		t.Run(tc.description, func(t *testing.T) {
			result := merge_ranges(tc.ranges)
			assert.Equal(t, tc.expected, result)
		})
	}
}
