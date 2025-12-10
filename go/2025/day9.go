package _2025

import (
	. "advent/data_structures/coord"
	"advent/utils"
	"fmt"
	"math"
	"slices"
	"strings"
)

func Day9Part1(input string) string {
	coords := parse_day9(input)
	max := 0
	for _, left := range coords {
		for _, right := range coords {
			area := rect_area(left, right)
			if area > max {max = area}
		}
	}
	return fmt.Sprint(max)
}
func Day9Part2(input string) string {
	return ""
}

func rect_area(c1, c2 Coord) int {
	dx := abs(c1.Dx(c2)) + 1
	dy := abs(c1.Dy(c2)) + 1
	return dx * dy
}

func abs(a int) int {
	return int(math.Abs(float64(a)))
}

func parse_day9(input string) []Coord {
	lines := slices.Collect(strings.Lines(input))
	lines = utils.Map(strings.TrimSpace, lines)
	return utils.Map(Coord{}.FromString, lines)
}
