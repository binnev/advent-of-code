package _2022

import (
	"sort"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSparseMatrixXsYs(t *testing.T) {
	grid := SparseMatrix{
		Coord{69, 420}:  '#',
		Coord{666, 888}: '#',
		Coord{777, 999}: '#',
	}
	xs := grid.xs()
	ys := grid.ys()
	sort.Ints(xs)
	sort.Ints(ys)
	assert.Equal(t, []int{69, 666, 777}, xs)
	assert.Equal(t, []int{420, 888, 999}, ys)
}

func TestSparseMatrixLimits(t *testing.T) {
	grid := SparseMatrix{
		Coord{69, 420}:  '#',
		Coord{666, 888}: '#',
		Coord{777, 999}: '#',
	}
	min, max := grid.Xlim()
	assert.Equal(t, min, 69)
	assert.Equal(t, max, 777)

	min, max = grid.Ylim()
	assert.Equal(t, min, 420)
	assert.Equal(t, max, 999)
}

func TestSparseMatrixToString(t *testing.T) {
	grid := SparseMatrix{
		Coord{0, 0}: 'A',
		Coord{2, 3}: 'B',
	}
	expected := strings.Join([]string{
		"A..",
		"...",
		"...",
		"..B",
	}, "\n")
	result := grid.ToString(false, 0, '.')
	assert.Equal(t, expected, result)
}

const FOO = `......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#..`

func TestSparseMatrixConstruct(t *testing.T) {
	grid := SparseMatrix{}
	for y, line := range strings.Split(FOO, "\n") {
		for x, value := range line {
			if value != '.' {
				grid[Coord{x, y}] = value
			}
		}
	}

	printed := grid.ToString(false, 0, '.')
	assert.Equal(t, printed, FOO)
}
