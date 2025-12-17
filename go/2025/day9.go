package _2025

import (
	. "advent/data_structures/coord"
	"advent/data_structures/matrix"
	"advent/data_structures/set"
	"advent/utils"
	"fmt"
	"iter"
	"slices"
	"sort"
	"strings"
)

func Day9Part1(input string) string {
	coords := parse_day9(input)
	rects := get_largest_rects(coords)
	max := rects[0]
	area := rect_area(max[0], max[1])
	return fmt.Sprint(area)
}

// We have several challenges now
// 1. We need to figure out which side of the loop is the inside
// 2. We need to fill the inside with green squares (BFS)

// 1. We will keep track of the compass direction of each edge. We will keep
// track of whether we turn CW or CCW when joining segments. That way we'll
// figure out if the right side or the left side is the inside.

func Day9Part2(input string) string {
	coords := parse_day9(input)
	filled := get_filled_shape(coords)
	rects := get_largest_rects(coords)
	for _, rect := range rects {
		left := rect[0]
		right := rect[1]
		if is_rect_filled(left, right, filled) {
			area := rect_area(left, right)
			return fmt.Sprint(area)
		}
	}
	panic("No filled rectangles!")
}

// Sort all possible rects by area descending
func get_largest_rects(coords []Coord) []Rect {
	edges := get_edges(coords)
	horizontal_edges, vertical_edges := sort_horizontal_vertical_edges(edges)
	rects := get_all_possible_rects(horizontal_edges, vertical_edges)
	sort.Slice(rects, func(i, j int) bool {
		left := rects[i]
		right := rects[j]
		left_area := rect_area(left[0], left[1])
		right_area := rect_area(right[0], right[1])
		return left_area > right_area
	})
	return rects
}

// To check if a rect is filled, we only need to check that the _sides_ are
// filled, because the filled shape does not have any holes.
func is_rect_filled(c1, c2 Coord, filled matrix.Matrix) bool {
	x1, y1 := c1.Unpack()
	x2, y2 := c2.Unpack()
	// check the horizontal sides
	for _, x := range my_range(x1, x2) {
		for _, y := range []int{y1, y2} {
			coord := Coord{x, y}
			if _, ok := filled[coord]; !ok {
				return false
			}
		}
	}
	// check the vertical sides
	for _, x := range []int{x1, x2} {
		for _, y := range my_range(y1, y2) {
			coord := Coord{x, y}
			if _, ok := filled[coord]; !ok {
				return false
			}
		}
	}
	return true
}

func rect_area(c1, c2 Coord) int {
	dx := c1.AbsDx(c2) + 1
	dy := c1.AbsDy(c2) + 1
	return dx * dy
}

func parse_day9(input string) []Coord {
	lines := slices.Collect(strings.Lines(input))
	lines = utils.Map(strings.TrimSpace, lines)
	return utils.Map(Coord{}.FromString, lines)
}

type Direction int

const (
	North Direction = iota
	East
	South
	West
)

// Get all the coords that fall inside the shape described by the puzzle input
func get_filled_shape(coords []Coord) matrix.Matrix {
	// Add the first coord to the end to close the loop
	coords = append(coords, coords[0])
	filled := matrix.Matrix{}
	// "draw" the lines connecting each coord
	for ii := 1; ii < len(coords); ii++ {
		x1, y1 := coords[ii-1].Unpack()
		x2, y2 := coords[ii].Unpack()
		for _, x := range my_range(x1, x2) {
			for _, y := range my_range(y1, y2) {
				coord := Coord{x, y}
				filled[coord] = '#'
			}
		}
	}
	// Add the first inside square and BFS to find them all
	inside_dir := get_inside_direction(coords)
	inside := get_inside_square(coords, inside_dir)
	frontier := matrix.Matrix{}
	frontier[inside] = 'X'
	for ii := 0; ii < 10; ii++ {

		filled = filled.Union(frontier)
		new_frontier := matrix.Matrix{}
		for coord := range frontier {
			for _, neighbour := range coord.CardinalNeighbours() {
				if !filled.Contains(neighbour) {
					new_frontier[neighbour] = 'X'
				}
			}
		}
		if len(new_frontier) == 0 {
			break
		}
		frontier = new_frontier
	}
	return filled
}

func my_range(from, to int) []int {
	if from == to {
		return []int{from}
	}
	var sign int
	switch {
	case to > from:
		sign = 1
	case to < from:
		sign = -1
	}
	out := []int{}
	for x := from; x != to; x += sign {
		out = append(out, x)
	}
	return out
}

// Get 1 square that's inside the loop, which we can use as a seed for BFS
func get_inside_square(coords []Coord, inside_direction LeftRight) Coord {
	current, next := get_first_edge_longer_than_2(coords)
	direction := get_edge_direction(current, next)

	var right int
	switch inside_direction {
	case Right:
		right = 1
	case Left:
		right = -1
	}

	x, y := current.Unpack()
	switch direction {
	case North:
		return Coord{x + right, y - 1}
	case East:
		return Coord{x + 1, y + right}
	case South:
		return Coord{x - right, y + 1}
	case West:
		return Coord{x - 1, y - right}
	default:
		panic("Unreachable")
	}
}

func get_first_edge_longer_than_2(coords []Coord) (Coord, Coord) {
	for ii := 1; ii < len(coords); ii++ {
		current := coords[ii-1]
		next := coords[ii]
		if current.TaxiCabDistance(next) < 2 {
			continue
		}
		return current, next
	}
	panic("Couldn't find 2 coords with a distance of >2?!")
}

// Count the left/right turns and work out if the loop curves to the right or
// the left. So if the first segment from point 0 to point 1 is going North,
// then we know that East is inside. Assume that the list of coords is "open"
// and we need to add the segment from last -> first.
func get_inside_direction(coords []Coord) LeftRight {
	edges := []Direction{}
	for ii := 1; ii < len(coords); ii++ {
		current := coords[ii-1]
		next := coords[ii]
		direction := get_edge_direction(current, next)
		edges = append(edges, direction)
	}

	turn_sum := 0
	for ii := 1; ii < len(edges); ii++ {
		current := edges[ii-1]
		next := edges[ii]
		turn := get_turn_direction(current, next)
		switch turn {
		case Right:
			turn_sum++
		case Left:
			turn_sum--
		}
	}
	switch {
	case turn_sum > 0:
		return Right
	case turn_sum < 0:
		return Left
	default:
		panic("Loop doesn't close!")
	}
}

// Given a current and next direction, figure out which direction we turned
func get_turn_direction(current, next Direction) LeftRight {
	x := map[[2]Direction]LeftRight{
		{North, East}: Right,
		{North, West}: Left,
		{East, South}: Right,
		{East, North}: Left,
		{South, West}: Right,
		{South, East}: Left,
		{West, North}: Right,
		{West, South}: Left,
	}
	if turn_direction, ok := x[[2]Direction{current, next}]; ok {
		return turn_direction
	}
	panic(fmt.Sprintf("Not a 90deg turn: %v to %v", current, next))
}

// Given the start and end point of an edge, figure out its compass direction
func get_edge_direction(p1, p2 Coord) Direction {
	if p1 == p2 {
		panic(fmt.Sprintf("Points are the same! %v, %v", p1, p2))
	}
	x1, y1 := p1.Unpack()
	x2, y2 := p2.Unpack()
	switch {
	case x1 == x2 && y2 > y1:
		return South // y is positive down
	case x1 == x2 && y2 < y1:
		return North
	case y1 == y2 && x2 > x1:
		return East
	case y1 == y2 && x2 < x1:
		return West
	}
	panic(fmt.Sprintf("Points are not aligned! %v, %v", p1, p2))
}

func get_unique_pairs[T comparable](values iter.Seq[T]) iter.Seq[[2]T] {
	return func(yield func([2]T) bool) {
		seen := set.Set[[2]T]{}
		for left := range values {
			for right := range values {
				pair := [2]T{left, right}
				reverse_pair := [2]T{right, left}
				if left == right ||
					seen.Contains(pair) ||
					seen.Contains(reverse_pair) {
					continue
				}
				seen.Add(pair)
				if !yield(pair) {
					return
				}
			}
		}
	}
}

type Edge [2]Coord

func get_edges(coords []Coord) []Edge {
	out := []Edge{}
	// Add the first coord to the end to lose the loop
	coords = append(coords, coords[0])
	for ii := 1; ii < len(coords); ii++ {
		current := coords[ii-1]
		next := coords[ii]
		edge := Edge{current, next}
		out = append(out, edge)
	}
	return out
}

func sort_horizontal_vertical_edges(edges []Edge) ([]Edge, []Edge) {
	horizontal := []Edge{}
	vertical := []Edge{}
	for _, edge := range edges {
		start, end := edge[0], edge[1]
		switch get_edge_direction(start, end) {
		case North | South:
			vertical = append(vertical, edge)
		case East | West:
			horizontal = append(horizontal, edge)
		}
	}
	return horizontal, vertical
}

type Rect [2]Coord

// Instead of considering all possible combos of _points_, consider all possible
// combos of horizontal/vertical _edges_ -- this gives us rectangles that are
// not possible when considering only points.
//
// Consider the below shape. The largest possible rectangle is one that doesn't
// share _any_ corners with the outside shape.
//
//	┏━━━┓  ┏━━━┓
//	┃   ┃  ┃   ┃
//	┃ ╭╴┗━━┛╴╮ ┃
//	┃ ┆      ┆ ┃
//	┗━┓      ┏━┛
//	  ┃      ┃
//	┏━┛      ┗━┓
//	┃ ┆      ┆ ┃
//	┃ ╰╴┏━━┓╴╯ ┃
//	┃   ┃  ┃   ┃
//	┗━━━┛  ┗━━━┛
func get_all_possible_rects(horizontal_edges, vertical_edges []Edge) []Rect {
	utils.Print("Got %v H edges", len(horizontal_edges))
	utils.Print("Got %v V edges", len(vertical_edges))
	unique_pairs_h := slices.Collect(get_unique_pairs(slices.Values(horizontal_edges)))
	unique_pairs_v := slices.Collect(get_unique_pairs(slices.Values(vertical_edges)))
	utils.Print("Found %v unique pairs of H edges", len(unique_pairs_h))
	utils.Print("Found %v unique pairs of V edges", len(unique_pairs_v))
	out := []Rect{}
	for h_edges := range get_unique_pairs(slices.Values(horizontal_edges)) {
		h_edge1 := h_edges[0]
		h_edge2 := h_edges[1]
		// utils.Print("Considering H edges %v, %v", h_edge1, h_edge2)

		h_coords := []Coord{h_edge1[0], h_edge1[1], h_edge2[0], h_edge2[1]}
		ys := utils.Map(func(c Coord) int { return c[1] }, h_coords)
		min_y := utils.Min(ys)
		max_y := utils.Max(ys)

		for v_edges := range get_unique_pairs(slices.Values(vertical_edges)) {
			v_edge1 := v_edges[0]
			v_edge2 := v_edges[1]
			// utils.Print("Considering V edges %v, %v", v_edge1, v_edge2)

			v_coords := []Coord{v_edge1[0], v_edge1[1], v_edge2[0], v_edge2[1]}
			xs := utils.Map(func(c Coord) int { return c[0] }, v_coords)
			min_x := utils.Min(xs)
			max_x := utils.Max(xs)

			coord1 := Coord{min_x, min_y}
			coord2 := Coord{max_x, max_y}
			rect := Rect{coord1, coord2}
			out = append(out, rect)
		}
	}
	return out
}
