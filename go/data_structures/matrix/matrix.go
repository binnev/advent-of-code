package matrix

import (
	. "advent/data_structures/coord"
	"advent/utils"
	"fmt"
	"strings"
)

// Sparse matrix type that doesn't store empty positions
type Matrix map[Coord]rune

func (m Matrix) xs() []int {
	xs := []int{}
	for coord := range m {
		xs = append(xs, coord[0])
	}
	return xs
}

func (m Matrix) ys() []int {
	ys := []int{}
	for coord := range m {
		ys = append(ys, coord[1])
	}
	return ys
}

func (m Matrix) Xlim() (int, int) {
	xs := m.xs()
	return utils.Min(xs), utils.Max(xs)
}

func (m Matrix) Ylim() (int, int) {
	ys := m.ys()
	return utils.Min(ys), utils.Max(ys)
}

func (m Matrix) ToString(flipY bool, pad int, emptyChar rune) string {
	minX, maxX, minY, maxY := 0, 0, 0, 0
	if len(m) > 0 {
		minX, maxX = m.Xlim()
		minY, maxY = m.Ylim()
	}
	lines := []string{}
	for y := minY - pad; y < maxY+1+pad; y++ {
		runes := []rune{}
		for x := minX - pad; x < maxX+1+pad; x++ {
			value, found := m[Coord{x, y}]
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

	matrix := Matrix.FromString("blabla", "")

but Go won't let you do this. A method must be attached to an _instance_ of a
type. So as a workaround you can call it like this:

	matrix := Matrix{}.FromString("blabla", "")

which creates an empty instance and then fills it using the FromString method.
It actually kinda makes sense; it's like the __new__ -> __init__ method calls in
python. __new__ creates an empty object, and __init__ sets the initial values.
*/
func (m Matrix) FromString(source string, ignore string) Matrix {
	for yy, line := range strings.Split(source, "\n") {
		for xx, char := range line {
			coord := Coord{xx, yy}
			if utils.Contains([]byte(ignore), byte(char)) {
				continue
			} else {
				m[coord] = char
			}
		}
	}
	return m
}

func (m Matrix) Print(flipY bool, pad int, emptyChar rune) {
	fmt.Println(m.ToString(flipY, pad, emptyChar))
}

func (m Matrix) Contains(coord Coord) bool {
	_, ok := m[coord]
	return ok
}

func (m Matrix) FindOne(needle rune) Coord {
	hits := []Coord{}
	for coord, value := range m {
		if value == needle {
			hits = append(hits, coord)
		}
	}
	if len(hits) == 0 {
		panic(fmt.Sprintf("Couldn't find %v!", needle))
	} else if len(hits) > 1 {
		panic(fmt.Sprintf("Multiple hits for %v: %v", needle, hits))
	}
	return hits[0]
}

func (m Matrix) Union(other Matrix) Matrix {
	for coord, val := range other {
		m[coord] = val
	}
	return m
}
