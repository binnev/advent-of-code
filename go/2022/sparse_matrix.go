package _2022

import (
	"fmt"
	"math"
	"strings"
)

type Coord [2]int
type Coord3 [3]int
type SparseMatrix map[Coord]rune
type SparseMatrix3 map[Coord3]rune

func (grid SparseMatrix) Xlim() (int, int) {
	min := math.Inf(1)
	max := math.Inf(-1)
	for coord, _ := range grid {
		x := float64(coord[0])
		if x < min {
			min = x
		}
		if x > max {
			max = x
		}
	}
	return int(min), int(max)
}

func (grid SparseMatrix) Ylim() (int, int) {
	min := math.Inf(1)
	max := math.Inf(-1)
	for coord, _ := range grid {
		x := float64(coord[1])
		if x < min {
			min = x
		}
		if x > max {
			max = x
		}
	}
	return int(min), int(max)
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
