package sparse_matrix

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
	lines := []string{}
	for y := minY - pad; y < maxY+1+pad; y++ {
		runes := []rune{}
		for x := minX - pad; x < maxX+1+pad; x++ {
			value, found := grid[Coord{x, y}]
			if !found {
				value = emptyChar
			}
			runes = append(runes, value)
		}
		lines = append(lines, string(runes))
	}
	if flipY {
		lines = utils.Reverse(lines)
	}
	return strings.Join(lines, "\n")
}

/*
I wanted a classmethod syntax like python:

	matrix := SparseMatrix.FromString("blabla", "")

but Go won't let you do this. A method must be attached to an _instance_ of a
type. So as a workaround you can call it like this:

	matrix := SparseMatrix{}.FromString("blabla", "")

which creates an empty instance and then fills it using the FromString method.
It actually kinda makes sense; it's like the __new__ -> __init__ method calls in
python. __new__ creates an empty object, and __init__ sets the initial values.
*/
func (matrix SparseMatrix) FromString(source string, ignore string) SparseMatrix {
	for yy, line := range strings.Split(source, "\n") {
		for xx, char := range line {
			coord := Coord{xx, yy}
			if utils.Contains([]byte(ignore), byte(char)) {
				continue
			} else {
				matrix[coord] = char
			}
		}
	}
	return matrix
}

func (grid SparseMatrix) Print(flipY bool, pad int, emptyChar rune) {
	fmt.Println(grid.ToString(flipY, pad, emptyChar))
}

func (grid SparseMatrix) Contains(coord Coord) bool {
	_, ok := grid[coord]
	return ok
}
