package _2022

import (
	. "advent/data_structures/coord"
	. "advent/data_structures/matrix"

	"fmt"
)

type Shape []Coord

var HLINE = Shape{
	{0, 0},
	{1, 0},
	{2, 0},
	{3, 0},
}

var PLUS = Shape{
	{1, 0},
	{0, 1},
	{1, 1},
	{1, 1},
	{1, 2},
	{2, 1},
}
var CORNER = Shape{
	{0, 0},
	{1, 0},
	{2, 0},
	{2, 1},
	{2, 2},
}
var VLINE = Shape{
	{0, 0},
	{0, 1},
	{0, 2},
	{0, 3},
}
var SQUARESHAPE = Shape{
	{0, 0},
	{0, 1},
	{1, 0},
	{1, 1},
}

var SHAPES = []Shape{HLINE, PLUS, CORNER, VLINE, SQUARESHAPE}

func copyShape(shape Shape) Shape {
	newShape := make(Shape, len(shape))
	copy(newShape, shape)
	return newShape
}

func spawnShape(index, x, y int) Shape {
	shape := copyShape(SHAPES[index])
	for ii := range shape {
		shape[ii][0] += x
		shape[ii][1] += y
	}
	return shape
}

func moveLeft(shape Shape, grid Matrix) Shape {
	newShape := copyShape(shape)
	for ii := range newShape {
		newShape[ii][0]--
	}
	for _, coord := range newShape {
		_, inGrid := grid[coord]
		x := coord[0]
		if inGrid || x < 0 {
			return shape
		}
	}
	return newShape
}

func moveRight(shape Shape, grid Matrix) Shape {
	newShape := copyShape(shape)
	for ii := range newShape {
		newShape[ii][0]++
	}
	for _, coord := range newShape {
		_, inGrid := grid[coord]
		x := coord[0]
		if inGrid || x > 6 {
			return shape
		}
	}
	return newShape
}

func fall(shape Shape, grid Matrix) (Shape, bool) {
	collision := false
	newShape := copyShape(shape)
	for ii := range newShape {
		newShape[ii][1]--
	}
	for _, coord := range newShape {
		_, exists := grid[coord]
		y := coord[1]
		if exists || y == 0 {
			collision = true
			return shape, collision
		}
	}
	return newShape, collision
}

func addShapeToTower(ii, jet_ii int, grid Matrix, jets string) (int, Shape) {
	// spawn rock at correct x/y
	towerHeight := 0
	if len(grid) > 0 {
		_, towerHeight = grid.Ylim()
	}
	x := 2
	y := 4 + towerHeight
	shape_ii := ii % len(SHAPES)
	shape := spawnShape(shape_ii, x, y)

	// move rock
	collision := false
	for !collision {
		// rock is moved by jets
		jet := jets[jet_ii]
		if jet == '>' {
			shape = moveRight(shape, grid)
		} else {
			shape = moveLeft(shape, grid)
		}

		// rock falls
		shape, collision = fall(shape, grid)
		jet_ii = (jet_ii + 1) % len(jets)
	}

	// add rock to tower
	for _, coord := range shape {
		grid[coord] = '#'
	}

	return jet_ii, shape
}

func buildTower(Nshapes int, jets string, grid Matrix) {
	jet_ii := 0
	for ii := 0; ii < Nshapes; ii++ {
		jet_ii, _ = addShapeToTower(ii, jet_ii, grid, jets)
	}
}

func printTower(grid, scenery Matrix) {
	forPrint := Matrix{}
	for key, value := range grid {
		forPrint[key] = value
	}
	for key, value := range scenery {
		forPrint[key] = value
	}
	forPrint.Print(true, 2, '.')
}

func Day17Part1(input string) string {
	grid := Matrix{}
	N := 2022
	buildTower(N, input, grid)
	_, bruteHeight := grid.Ylim()
	return fmt.Sprint(bruteHeight)
}
