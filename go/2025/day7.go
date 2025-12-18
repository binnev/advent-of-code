package _2025

import (
	. "advent/data_structures/coord"
	"advent/data_structures/matrix"
	"fmt"
)

const (
	EMPTY    = '.'
	START    = 'S'
	SPLITTER = '^'
)

func Day7Part1(input string) string {
	grid := matrix.FromString(input, "")
	beams := map[Coord]int{}
	beams[grid.FindOne('S')] = 1
	_, total := run_beams(grid, beams)
	return fmt.Sprint(total)
}

func Day7Part2(input string) string {
	grid := matrix.FromString(input, "")
	beams := map[Coord]int{}
	beams[grid.FindOne('S')] = 1
	beams, _ = run_beams(grid, beams)
	total := 0
	for _, n_beams := range beams {
		total += n_beams
	}
	return fmt.Sprint(total)
}

// Iterate the beams until they're finished. Return a map of coordinates of new
// beams, and the number of beams that occupy each coordinate. Also return the
// number of times a beam was split.
func run_beams(grid matrix.Matrix, beams map[Coord]int) (map[Coord]int, int) {
	total_n_splits := 0

	// using := in the loop results in `beams` not being updated in the loop!
	var n_splits int
	var new_beams map[Coord]int

	for {
		new_beams, n_splits = iterate_beams(grid, beams)
		total_n_splits += n_splits
		if len(new_beams) == 0 {
			break
		}
		beams = new_beams
	}
	return beams, total_n_splits
}

// Iterate the beams 1 tick. Return a map of coordinates of new beams, and the
// number of beams that occupy each coordinate. Also return the number of
// times a beam was split.
func iterate_beams(grid matrix.Matrix, beams map[Coord]int) (map[Coord]int, int) {
	out := map[Coord]int{}
	n_splits := 0
	for coord, n_beams := range beams {
		new_beams := iterate_beam(grid, coord)
		if len(new_beams) > 1 {
			n_splits++
		}
		for _, new_beam := range new_beams {
			out[new_beam] += n_beams
		}
	}
	return out, n_splits
}

// Iterate 1 beam 1 tick. Beams continue straight down unless they hit a
// splitter or exit the grid
func iterate_beam(grid matrix.Matrix, beam Coord) []Coord {
	below := Coord{beam[0], beam[1] + 1}
	value, ok := grid[below]

	// If the new coord is not in the grid, the beam has left the grid, and we
	// should return empty
	if !ok {
		return []Coord{}
	}

	// If the new coord is empty, the beam should move into that space
	if value == EMPTY {
		return []Coord{below}
	}

	// If the new coord contains a splitter, we should spawn a new beam to
	// either side of the splitter (provided that both coords are in the grid)
	if value == SPLITTER {
		out := []Coord{}
		left := Coord{below[0] - 1, below[1]}
		right := Coord{below[0] + 1, below[1]}
		if grid.Contains(left) {
			out = append(out, left)
		}
		if grid.Contains(right) {
			out = append(out, right)
		}
		return out
	}

	panic(fmt.Sprintf("Unrecognised value %v", value))
}
