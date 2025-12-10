package _2025

import (
	. "advent/data_structures/coord"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day9 = `7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3`

func TestDay9Part1(t *testing.T) {
	assert.Equal(t, "50", Day9Part1(example_day9))
}
func Test_rect_area(t *testing.T) {
	testcases := []struct {
		c1, c2   string
		expected int
	}{
		{"0, 0", "0, 0", 1},
		{"2,5", "9,7", 24},
		{"7,1", "11,7", 35},
		{"7,3", "2,3", 6},
		{"2,5", "11,1", 50},
	}
	for _, tc := range testcases {
		t.Run(fmt.Sprintf("%v_to_%v", tc.c1, tc.c2), func(t *testing.T) {
			coord1 := Coord{}.FromString(tc.c1)
			coord2 := Coord{}.FromString(tc.c2)
			result := rect_area(coord1, coord2)
			assert.Equal(t, tc.expected, result)
		})
	}
}
