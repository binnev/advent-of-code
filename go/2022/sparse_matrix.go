package _2022

import (
	"advent/utils"
	"fmt"
	"strings"
)

type Coord [2]int
type Coord3 [3]int
type SparseMatrix map[Coord]rune
type SparseMatrix3 map[Coord3]rune

func (grid SparseMatrix) xs() []int {
	xs := []int{}
	for coord, _ := range grid {
		xs = append(xs, coord[0])
	}
	return xs
}

func (grid SparseMatrix) ys() []int {
	ys := []int{}
	for coord, _ := range grid {
		ys = append(ys, coord[1])
	}
	return ys
}

func (grid SparseMatrix) Xlim() (int, int) {
	xs := grid.xs()
	return utils.Min(xs), utils.Max(xs)
}

func (grid SparseMatrix) Ylim() (int, int) {
	ys := grid.ys()
	return utils.Min(ys), utils.Max(ys)
}

func (grid SparseMatrix) ToString(flipY bool, pad int, emptyChar rune) string {
	minX, maxX, minY, maxY := 0, 0, 0, 0
	if len(grid) > 0 {
		minX, maxX = grid.Xlim()
		minY, maxY = grid.Ylim()
	}
	if flipY {
		minY, maxY = -maxY, -minY
	}

	outputLines := []string{}
	for y := minY - pad; y < maxY+1+pad; y++ {
		lineRunes := []rune{}
		for x := minX - pad; x < maxX+1+pad; x++ {
			if flipY {
				y = -y
			}
			value, found := grid[Coord{x, y}]
			if !found {
				value = emptyChar
			}
			lineRunes = append(lineRunes, value)
		}
		line := string(lineRunes)
		outputLines = append(outputLines, line)
	}
	output := strings.Join(outputLines, "\n")
	return output
}

func (grid SparseMatrix) Print(flipY bool, pad int, emptyChar rune) {
	fmt.Println(grid.ToString(flipY, pad, emptyChar))
}
