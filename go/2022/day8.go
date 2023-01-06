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

func isVisibleInRow(x int, row []int) bool {
	height := row[x]
	left := row[:x]
	right := row[x+1:]
	leftVisible := true
	rightVisible := true
	for _, tree := range left {
		if tree >= height {
			leftVisible = false
			break
		}
	}
	for _, tree := range right {
		if tree >= height {
			rightVisible = false
			break
		}
	}
	return leftVisible || rightVisible
}

func getCol(x int, grid TreeGrid) []int {
	col := []int{}
	for _, row := range grid {
		col = append(col, row[x])
	}
	return col
}

func isVisibleFromEdge(x int, y int, grid TreeGrid) bool {
	col := getCol(x, grid)
	row := grid[y]
	return isVisibleInRow(x, row) || isVisibleInRow(y, col)
}

func scenicScoreRow(x int, row []int) int {
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

func scenicScore(x, y int, grid TreeGrid) int {
	col := getCol(x, grid)
	row := grid[y]
	rowScore := scenicScoreRow(x, row)
	colScore := scenicScoreRow(y, col)
	return rowScore * colScore
}

func Day8Part1() string {
	// input := example
	input := utils.LoadPuzzleInput("2022/day8")
	grid := parseTreeGrid(input)
	count := 0
	for y, row := range grid {
		for x := range row {
			if isVisibleFromEdge(x, y, grid) {
				count += 1
			}
		}
	}
	return fmt.Sprint(count)
}

func Day8Part2() string {
	// input := example
	input := utils.LoadPuzzleInput("2022/day8")
	grid := parseTreeGrid(input)
	maxScore := 0
	for y, row := range grid {
		for x := range row {
			score := scenicScore(x, y, grid)
			if score > maxScore {
				maxScore = score
			}
		}
	}
	return fmt.Sprint(maxScore)
}

func Day8() {
	utils.Profile(Day8Part1)
	utils.Profile(Day8Part2)
}
