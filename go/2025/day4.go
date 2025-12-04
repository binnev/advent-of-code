package _2025

import (
	. "advent/data_structures/sparse_matrix"
	"advent/utils"
	"fmt"
)

const ROLL = '@'

func Day4Part1(input string) string {
	grid := SparseMatrix{}.FromString(input, ".")
	utils.Print("len(grid) = %v", len(grid))
	total := 0
	for coord, value := range grid {
		if value != ROLL {
			continue
		}
		adjacent_rolls := count_adjacent_rolls(grid, coord)
		if adjacent_rolls < 4 {
			total++
		}
	}
	return fmt.Sprint(total)
}
func Day4Part2(input string) string {
	return ""
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
