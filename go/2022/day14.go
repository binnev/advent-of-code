package _2022

import (
	. "advent/data_structures/sparse_matrix"
	. "advent/data_structures/coord"

	"advent/utils"
	"fmt"
	"strings"
)

const (
	FALLING   = 0
	RESTING   = 1
	DESTROYED = 2
	WALL      = '█'
	SAND      = '░'
)

func drawLine(start, end Coord, grid SparseMatrix) {
	startX, startY := start[0], start[1]
	endX, endY := end[0], end[1]
	dy := endY - startY
	if startX > endX {
		startX, endX = endX, startX
	}
	if startY > endY {
		startY, endY = endY, startY
	}
	if dy == 0 {
		for x := startX; x < endX+1; x++ {
			coord := Coord{x, startY}
			grid[coord] = WALL
		}
	} else {
		for y := startY; y < endY+1; y++ {
			coord := Coord{startX, y}
			grid[coord] = WALL
		}
	}
}

func parseDay14Input(input string) SparseMatrix {
	instructions := strings.Split(input, "\n")
	grid := SparseMatrix{}
	for _, ins := range instructions {
		points := []Coord{}
		for _, pointStr := range strings.Split(ins, " -> ") {
			xy := strings.Split(pointStr, ",")
			x := utils.ParseInt(xy[0])
			y := utils.ParseInt(xy[1])
			points = append(points, Coord{x, y})
		}
		for ii := 0; ii < len(points)-1; ii++ {
			start := points[ii]
			end := points[ii+1]
			drawLine(start, end, grid)
		}
	}
	return grid
}

func sandStep(
	pos Coord,
	grid SparseMatrix,
	floor int, // y-height of the floor
	solidFloor bool, // can the sand come to rest on the floor
) (newPos Coord, status int) {
	x, y := pos[0], pos[1]
	options := []Coord{
		{x, y + 1},
		{x - 1, y + 1},
		{x + 1, y + 1},
	}
	for _, coord := range options {
		y := coord[1]
		_, occupied := grid[coord]
		if !occupied {
			if y == floor {
				if solidFloor {
					return pos, RESTING
				} else {
					return pos, DESTROYED
				}
			} else {
				return coord, FALLING
			}
		}
	}
	return pos, RESTING
}

func sandTrace(origin Coord, grid SparseMatrix, floor int, solidFloor bool) int {
	// return True if sand came to rest OK; false if it fell off the map
	pos := origin
	status := FALLING
	for status == FALLING {
		pos, status = sandStep(pos, grid, floor, solidFloor)
	}
	if status == RESTING {
		grid[pos] = SAND
	}
	return status
}

func Day14Part1(input string) string {
	grid := parseDay14Input(input)
	origin := Coord{500, 0}
	_, abyss := grid.Ylim()
	ii := 0
	for {
		status := sandTrace(origin, grid, abyss, false)
		if status == DESTROYED {
			break
		}
		ii++
	}
	return fmt.Sprint(ii)
}

func Day14Part2(input string) string {
	grid := parseDay14Input(input)
	origin := Coord{500, 0}
	_, maxY := grid.Ylim()
	floor := 2 + maxY
	ii := 0
	for {
		status := sandTrace(origin, grid, floor, true)
		if status == DESTROYED {
			break
		}
		ii++
		_, ok := grid[origin]
		if ok {
			break
		}
	}
	return fmt.Sprint(ii)
}
