package _2025

import (
	. "advent/data_structures/coord"
	. "advent/data_structures/sparse_matrix"
	"fmt"
)

const ROLL = '@'

func Day4Part1(input string) string {
	grid := SparseMatrix{}.FromString(input, ".")
	total := 0
	for coord := range grid {
		if count_adjacent_rolls(grid, coord) < 4 {
			total++
		}
	}
	return fmt.Sprint(total)
}
func Day4Part2(input string) string {
	grid := SparseMatrix{}.FromString(input, ".")
	total := 0
	for {
		removed := remove_rolls(&grid)
		total += removed
		if removed == 0 {
			break
		}
	}
	return fmt.Sprint(total)
}

func remove_rolls(grid *SparseMatrix) int {
	// First identify the removable ones without removing them, so there's no
	// race conditions
	removable := []Coord{}
	for coord := range *grid {
		if count_adjacent_rolls(*grid, coord) < 4 {
			removable = append(removable, coord)
		}
	}
	// Then remove them all at once
	for _, coord := range removable {
		delete(*grid, coord)
	}
	return len(removable)
}

func count_adjacent_rolls(grid SparseMatrix, coord Coord) int {
	x, y := coord[0], coord[1]
	neighbours := [8]Coord{
		{x - 1, y - 1},
		{x - 1, y},
		{x - 1, y + 1},
		{x, y - 1},
		{x, y + 1},
		{x + 1, y - 1},
		{x + 1, y},
		{x + 1, y + 1},
	}
	total := 0
	for _, neighbour := range neighbours {
		value := grid[neighbour]
		if value == ROLL {
			total++
		}
	}
	return total
}
