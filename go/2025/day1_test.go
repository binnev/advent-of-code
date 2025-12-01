package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day1 = `L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`

func Test_Day1Part1(t *testing.T) {
	assert.Equal(t, "3", Day1Part1(example_day1))
}

func Test_Day1Part2(t *testing.T) {
	assert.Equal(t, "6", Day1Part2(example_day1))
}

func Test_parse_dial_instruction(t *testing.T) {
	dir, n := parse_dial_instruction("L30")
	assert.Equal(t, Left, dir)
	assert.Equal(t, 30, n)
}

func Test_move_dial(t *testing.T) {
	testscases := []struct {
		description         string
		dial                int
		n                   int
		max                 int
		dir                 Direction
		expected_dial       int
		expected_zero_count int
	}{
		{
			description:         "right 0",
			dial:                0,
			n:                   0,
			dir:                 Right,
			expected_dial:       0,
			expected_zero_count: 0, // because we didn't move
		},
		{
			description:         "right 1",
			dial:                0,
			n:                   1,
			dir:                 Right,
			expected_dial:       1,
			expected_zero_count: 0,
		},
		{
			description:         "right 1 edge",
			dial:                98,
			n:                   1,
			dir:                 Right,
			expected_dial:       99,
			expected_zero_count: 0,
		},
		{
			description:         "right 99",
			dial:                0,
			n:                   99,
			dir:                 Right,
			expected_dial:       99,
			expected_zero_count: 0,
		},
		{
			description:         "right 1 cross",
			dial:                99,
			n:                   1,
			dir:                 Right,
			expected_dial:       0,
			expected_zero_count: 1,
		},
		{
			description:         "left 1",
			dial:                99,
			n:                   1,
			dir:                 Left,
			expected_dial:       98,
			expected_zero_count: 0,
		},
		{
			description:         "left 1 edge",
			dial:                1,
			n:                   1,
			dir:                 Left,
			expected_dial:       0,
			expected_zero_count: 1,
		},
		{
			description:         "left 0",
			dial:                0,
			n:                   0,
			dir:                 Left,
			expected_dial:       0,
			expected_zero_count: 0, // because we didn't move
		},
		{
			description:         "left 99",
			dial:                99,
			n:                   99,
			dir:                 Left,
			expected_dial:       0,
			expected_zero_count: 1,
		},
		{
			description:         "left 1 cross",
			dial:                0,
			n:                   1,
			dir:                 Left,
			expected_dial:       99,
			expected_zero_count: 0,
		},
		{
			description:         "left whole rotation",
			dial:                0,
			n:                   100,
			dir:                 Left,
			expected_dial:       0,
			expected_zero_count: 1,
		},
		{
			description:         "left 2 whole rotation",
			dial:                0,
			n:                   200,
			dir:                 Left,
			expected_dial:       0,
			expected_zero_count: 2,
		},
		{
			description:         "right whole rotation",
			dial:                0,
			n:                   100,
			dir:                 Right,
			expected_dial:       0,
			expected_zero_count: 1,
		},
		{
			description:         "right 2 whole rotation",
			dial:                0,
			n:                   200,
			dir:                 Right,
			expected_dial:       0,
			expected_zero_count: 2,
		},
	}
	for _, tc := range testscases {
		t.Run(tc.description, func(t *testing.T) {
			dial, zero_count := move_dial(tc.dial, tc.n, tc.dir)
			assert.Equal(t, tc.expected_dial, dial)
			assert.Equal(t, tc.expected_zero_count, zero_count)
		})
	}
}
