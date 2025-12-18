package matrix

import (
	. "advent/data_structures/coord"
	"advent/utils"
	"fmt"
	"iter"
	"maps"
	"strings"
)

// Sparse matrix type that doesn't store empty positions
type Matrix map[Coord]rune

func (m Matrix) Contains(coord Coord) bool {
	_, ok := m[coord]
	return ok
}

func (m Matrix) ContainsVal(needle rune) bool {
	for _, val := range m {
		if val == needle {
			return true
		}
	}
	return false
}

// Find the coord for the given value. Panics if there isn't exactly one of the
// given value in the matrix.
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

// Equivalent of python dict.update(other_dict).
// On collisions, values from the other matrix take precedence.
func (m Matrix) Union(other Matrix) Matrix {
	for coord, val := range other {
		m[coord] = val
	}
	return m
}

func (m Matrix) Limits() (x_min, x_max, y_min, y_max int) {
	if len(m) == 0 {
		panic("Can't get limits of empty Matrix!")
	}
	for coord := range m {
		x, y := coord.Unpack()
		x_min, x_max, y_min, y_max = x, x, y, y
		break
	}
	for coord := range m {
		x, y := coord.Unpack()
		if x < x_min {
			x_min = x
		}
		if x > x_max {
			x_max = x
		}
		if y < y_min {
			y_min = y
		}
		if y > y_max {
			y_max = y
		}
	}
	return
}
func (m Matrix) Xlim() (x_min, x_max int) {
	x_min, x_max, _, _ = m.Limits()
	return
}

func (m Matrix) Ylim() (y_min, y_max int) {
	_, _, y_min, y_max = m.Limits()
	return
}

func (m Matrix) Xs() iter.Seq[int] {
	return func(yield func(int) bool) {
		for coord := range m {
			if !yield(coord[0]) {
				return
			}
		}
	}
}

func (m Matrix) Ys() iter.Seq[int] {
	return func(yield func(int) bool) {
		for coord := range m {
			if !yield(coord[1]) {
				return
			}
		}
	}
}

// ================================= iter stuff ================================
func (m Matrix) Keys() iter.Seq[Coord] {
	return maps.Keys(m)
}
func (m Matrix) Values() iter.Seq[rune] {
	return maps.Values(m)
}
func (m Matrix) All() iter.Seq2[Coord, rune] {
	return maps.All(m)
}
func (m *Matrix) Insert(seq iter.Seq2[Coord, rune]) {
	maps.Insert(*m, seq)
}

// ================================ string stuff ===============================

func (m Matrix) String() string {
	return m.ToString(false, 0, '.')
}

var _ fmt.Stringer = (*Matrix)(nil)

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

// ALL runes in the ignore string will be ignored.
func FromString(source string, ignore string) Matrix {
	m := Matrix{}
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
