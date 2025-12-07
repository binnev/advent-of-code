package _2025

import (
	. "advent/data_structures/sparse_matrix"
	"advent/utils"
	"fmt"
)

const (
	EMPTY    = '.'
	START    = 'S'
	SPLITTER = '^'
)

func Day7Part1(input string) string {
	// Read input to sparse matrix
	grid := SparseMatrix{}.FromString(input, "")
	beams := []Coord{}
	for coord, value := range grid {
		if value == START {
			beams = append(beams, coord)
		}
	}
	// Iterate beams until they all reach the bottom
	total := 0
	n_splits := 0 // using := in the loop results in `beams` not being updated in the loop!
	for {
		beams, n_splits = iterate_beams(grid, beams)
		total += n_splits
		if len(beams) == 0 {
			break
		}
	}

	return fmt.Sprint(total)
}
func Day7Part2(input string) string {
	return ""
}

// Iterate the beams 1 tick. Return the de-duped list of new beams. Also return
// the number of times a beam was split.
func iterate_beams(grid SparseMatrix, beams []Coord) ([]Coord, int) {
	out := []Coord{}
	n_splits := 0
	for _, beam := range beams {
		new_beams := iterate_beam(grid, beam)
		if len(new_beams) > 1 {
			n_splits++
		}
		for _, new_beam := range new_beams {
			if !utils.Contains(out, new_beam) {
				out = append(out, new_beam)
			}
		}
	}
	return out, n_splits
}

// Iterate 1 beam 1 tick. Beams continue straight down unless they hit a
// splitter or exit the grid
func iterate_beam(grid SparseMatrix, beam Coord) []Coord {
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
