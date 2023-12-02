package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type TreeGrid [][]int

func parseTreeGrid(input string) TreeGrid {
	grid := TreeGrid{}
	for _, rowStr := range strings.Split(input, "\n") {
		row := []int{}
		for _, heightStr := range rowStr {
			height := utils.ParseInt(string(heightStr))
			row = append(row, height)
		}
		grid = append(grid, row)
	}
	return grid
}

func getCol(x int, grid TreeGrid) []int {
	col := []int{}
	for _, row := range grid {
		col = append(col, row[x])
	}
	return col
}

// Is the tree visible in a 1D array of trees
func isVisible1D(x int, row []int) bool {
	height := row[x]
	left := row[:x]
	right := row[x+1:]
	for _, side := range [][]int{left, right} {
		visible := true
		for _, tree := range side {
			if tree >= height {
				visible = false
				break
			}
		}
		if visible {
			return true
		}
	}
	return false
}

// Is the tree visible in a 2D array of trees
func isVisible2D(x int, y int, grid TreeGrid) bool {
	col := getCol(x, grid)
	row := grid[y]
	return isVisible1D(x, row) || isVisible1D(y, col)
}

func scenicScore1D(x int, row []int) int {
	height := row[x]
	left := row[:x]
	right := row[x+1:]
	lScore, rScore := 0, 0
	for ii := len(left) - 1; ii >= 0; ii-- {
		tree := left[ii]
		lScore += 1
		if tree >= height {
			break
		}
	}
	for _, tree := range right {
		rScore += 1
		if tree >= height {
			break
		}
	}
	return lScore * rScore
}

func scenicScore2D(x, y int, grid TreeGrid) int {
	col := getCol(x, grid)
	row := grid[y]
	rowScore := scenicScore1D(x, row)
	colScore := scenicScore1D(y, col)
	return rowScore * colScore
}

func Day8Part1(input string) string {
	grid := parseTreeGrid(input)
	count := 0
	for y, row := range grid {
		for x := range row {
			if isVisible2D(x, y, grid) {
				count += 1
			}
		}
	}
	return fmt.Sprint(count)
}

func Day8Part2(input string) string {
	grid := parseTreeGrid(input)
	maxScore := 0
	for y, row := range grid {
		for x := range row {
			score := scenicScore2D(x, y, grid)
			if score > maxScore {
				maxScore = score
			}
		}
	}
	return fmt.Sprint(maxScore)
}
