package _2015

import (
	. "advent/data_structures/sparse_matrix"
	"fmt"
)

func Day3Part1(input string) string {
	presents := count_presents_per_location(input)
	return fmt.Sprint(len(presents))
}
func Day3Part2(input string) string {
	return ""
}

func count_presents_per_location(input string) SparseMatrix {
	presents := SparseMatrix{}
	pos := Coord{0, 0}
	for _, arrow := range input {
		pos = update_pos_with_arrow(pos, arrow)
		presents[pos] += 1
	}
	return presents
}

func update_pos_with_arrow(pos Coord, arrow rune) Coord {
	switch arrow {
	case '>':
		return Coord{pos[0] + 1, pos[1]}
	case '<':
		return Coord{pos[0] - 1, pos[1]}
	case 'v':
		return Coord{pos[0], pos[1] + 1}
	case '^':
		return Coord{pos[0], pos[1] - 1}
	default:
		panic(fmt.Sprintf("Unrecognised rune: %v", arrow))
	}
}
