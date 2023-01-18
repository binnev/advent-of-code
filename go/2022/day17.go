package _2022

import (
	"advent/utils"
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

func moveLeft(shape Shape, grid SparseMatrix) Shape {
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

func moveRight(shape Shape, grid SparseMatrix) Shape {
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

func fall(shape Shape, grid SparseMatrix) (Shape, bool) {
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

func addShapeForPrint(shape Shape, grid SparseMatrix) {
	for _, coord := range shape {
		grid[coord] = '@'
	}
}

func removeShapeForPrint(shape Shape, grid SparseMatrix) {
	for _, coord := range shape {
		delete(grid, coord)
	}
}

func addShapeToTower(ii, jet_ii int, grid SparseMatrix, jets string) (int, Shape) {
	// spawn rock at correct x/y
	towerHeight := 0
	if len(grid) > 0 {
		towerHeight = utils.Max(grid.ys())
	}
	x := 2
	y := 4 + towerHeight
	shape_ii := ii % len(SHAPES)
	shape := copyShape(SHAPES[shape_ii])
	for ii := range shape {
		shape[ii][0] += x
		shape[ii][1] += y
	}

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

func buildTower(Nshapes int, jets string, grid SparseMatrix) {
	jet_ii := 0
	for ii := 0; ii < Nshapes; ii++ {
		jet_ii, _ = addShapeToTower(ii, jet_ii, grid, jets)
	}
}

func printTower(grid, scenery SparseMatrix) {
	forPrint := SparseMatrix{}
	for key, value := range grid {
		forPrint[key] = value
	}
	for key, value := range scenery {
		forPrint[key] = value
	}
	forPrint.Print(true, 2, '.')
}

func Day17Part1() string {
	jets := utils.LoadPuzzleInput("2022/day17")
	grid := SparseMatrix{}
	N := 2022
	buildTower(N, jets, grid)
	bruteHeight := utils.Max(grid.ys())
	return fmt.Sprint(bruteHeight)
}
