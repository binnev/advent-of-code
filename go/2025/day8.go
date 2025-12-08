package _2025

import (
	"advent/data_structures/set"
	. "advent/data_structures/sparse_matrix"
	"strconv"
	"strings"
)

func Day8Part1(input string) string {

	return ""
}
func Day8Part2(input string) string {
	return ""
}

type Circuit map[Coord3]bool

func foo(boxes set.Set[Coord3], n_connections int) []Circuit {
	circuits := []Circuit{}

	return circuits
}

func parse_day8(input string) set.Set[Coord3] {
	s := set.Set[Coord3]{}
	for line := range strings.Lines(input) {
		parts := strings.Split(line, ",")
		x, _ := strconv.Atoi(parts[0])
		y, _ := strconv.Atoi(parts[1])
		z, _ := strconv.Atoi(parts[2])
		coord := Coord3{x, y, z}
		s.Add(coord)
	}
	return s
}
