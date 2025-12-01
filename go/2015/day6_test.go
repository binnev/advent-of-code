package _2015

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_LightGrid(t *testing.T) {
	grid := LightGrid{}
	assert.Equal(t, 1000, len(grid))
	assert.Equal(t, 1000, len(grid[0]))
}

func Test_change(t *testing.T) {
	testcases := []struct {
		description string
		grid        LightGrid
		rect        Rect
		expected    int
	}{
		{
			description: "turn on all",
			rect:        Rect{0, 0, 999, 999},
			expected:    1_000_000,
		},
		{
			description: "turn on first line",
			rect:        Rect{0, 0, 999, 0},
			expected:    1_000,
		},
		{
			description: "turn on middle 4",
			rect:        Rect{499, 499, 500, 500},
			expected:    4,
		},
	}
	for _, tc := range testcases {
		t.Run(tc.description, func(t *testing.T) {
			grid := LightGrid{}
			grid.change(tc.rect, TurnOn)
			assert.Equal(t, tc.expected, grid.count())
		})
	}

}

func Test_parse_light_action(t *testing.T) {
	assert.Equal(t,
		TurnOn,
		parse_light_action("turn on 887,9 through 959,629"),
	)
	assert.Equal(t,
		TurnOff,
		parse_light_action("turn off 150,300 through 213,740"),
	)
	assert.Equal(t,
		Toggle,
		parse_light_action("toggle 846,296 through 969,528"),
	)
}

func Test_parse_rect(t *testing.T) {
	assert.Equal(t,
		Rect{887, 9, 959, 629},
		parse_rect("turn on 887,9 through 959,629"),
	)
	assert.Equal(t,
		Rect{150, 300, 213, 740},
		parse_rect("turn off 150,300 through 213,740"),
	)
	assert.Equal(t,
		Rect{846, 296, 969, 528},
		parse_rect("toggle 846,296 through 969,528"),
	)
}
