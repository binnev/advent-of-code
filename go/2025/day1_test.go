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
		description string
		dial        int
		n           int
		max         int
		dir         Direction
		expected    int
	}{
		{
			description: "right 1",
			dial:        0,
			n:           1,
			max:         100,
			dir:         Right,
			expected:    1,
		},
		{
			description: "right 99",
			dial:        0,
			n:           99,
			max:         100,
			dir:         Right,
			expected:    99,
		},
		{
			description: "right 1 cross",
			dial:        99,
			n:           1,
			max:         100,
			dir:         Right,
			expected:    0,
		},
		{
			description: "left 1",
			dial:        99,
			n:           1,
			max:         100,
			dir:         Left,
			expected:    98,
		},
		{
			description: "left 99",
			dial:        99,
			n:           99,
			max:         100,
			dir:         Left,
			expected:    0,
		},
		{
			description: "left 1 cross",
			dial:        0,
			n:           1,
			max:         100,
			dir:         Left,
			expected:    99,
		},
		{
			description: "left whole rotation",
			dial:        0,
			n:           100,
			max:         100,
			dir:         Left, expected: 0,
		},
	}
	for _, tc := range testscases {
		t.Run(tc.description, func(t *testing.T) {
			assert.Equal(t, tc.expected, move_dial(
				tc.dial, tc.n, tc.max, tc.dir,
			))
		})
	}
}
