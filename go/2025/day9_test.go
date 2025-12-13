package _2025

import (
	. "advent/data_structures/coord"
	"advent/data_structures/matrix"
	"advent/utils"
	"fmt"
	"slices"
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

const example_day9_filled = `..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............`

func TestDay9Part1(t *testing.T) {
	assert.Equal(t, "50", Day9Part1(example_day9))
}
func TestDay9Part2(t *testing.T) {
	assert.Equal(t, "24", Day9Part2(example_day9))
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

func Test_get_inside_direction(t *testing.T) {
	coords := parse_day9(example_day9)
	result := get_inside_direction(coords)
	assert.Equal(t, Right, result)
}

func Test_get_inside_square(t *testing.T) {
	coords := parse_day9(example_day9)
	result := get_inside_square(coords, Right)
	assert.Equal(t, Coord{8, 2}, result)
}

func Test_get_filled_squares(t *testing.T) {
	utils.Print("Sanity check")
	coords := parse_day9(example_day9)
	filled := get_filled_squares(coords)
	mat := matrix.Matrix{}.FromString(example_day9_filled, ".")
	assert.Equal(t, len(mat), len(filled))
}

func Test_is_rect_filled(t *testing.T) {
	coords := parse_day9(example_day9)
	filled := get_filled_squares(coords)
	testcases := []struct {
		c1, c2   string
		expected bool
	}{
		{"7,3", "11,1", true},
		{"2,5", "11,1", false},
		{"9,5", "2,3", true},
		{"9,7", "9,5", true},
	}
	for _, tc := range testcases {
		coord1 := Coord{}.FromString(tc.c1)
		coord2 := Coord{}.FromString(tc.c2)
		t.Run(fmt.Sprintf("%v-%v", tc.c1, tc.c2), func(t *testing.T) {
			result := is_rect_filled(coord1, coord2, filled)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func Test_get_unique_pairs(t *testing.T) {
	arr := []Coord{{1, 1}, {2, 2}, {3, 3}}
	result := slices.Collect(get_unique_pairs(slices.Values(arr)))
	expected := [][2]Coord{
		{Coord{1, 1}, Coord{2, 2}},
		{Coord{1, 1}, Coord{3, 3}},
		{Coord{2, 2}, Coord{3, 3}},
	}
	utils.Print("expected:\n%v", expected)
	utils.Print("result:\n%v", result)
	assert.Equal(t, 3, len(result))
	assert.Equal(t, expected, result)
}
