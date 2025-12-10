package _2015

import (
	. "advent/data_structures/coord"
	. "advent/data_structures/sparse_matrix"
	"fmt"
)

func Day3Part1(input string) string {
	presents := deliver_presents(input, 1)
	return fmt.Sprint(len(presents))
}
func Day3Part2(input string) string {
	presents := deliver_presents(input, 2)
	return fmt.Sprint(len(presents))
}

func deliver_presents(input string, n_workers int) SparseMatrix {
	presents := SparseMatrix{}
	workers := make([]Coord, n_workers)
	for ii, arrow := range input {
		worker_index := ii % n_workers
		pos := workers[worker_index]
		workers[worker_index] = update_pos_with_arrow(pos, arrow)
		for _, pos := range workers {
			presents[pos] += 1
		}
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
