package _2025

import (
	. "advent/data_structures/coord"
	"advent/data_structures/matrix"
	"advent/data_structures/set"
	"advent/utils"
	"fmt"
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
	utils.Print("Calculating filled squares...")
	filled := get_filled_squares(coords)
	utils.Print("Calculating largest rects...")
	rects := get_largest_rects(coords)
	for _, rect := range rects {
		utils.Print("Considering rect %v", rect)
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
func get_largest_rects(coords []Coord) []Edge {
	out := get_unique_edges(coords).ToSlice()
	sort.Slice(out, func(i, j int) bool {
		left := out[i]
		right := out[j]
		left_area := rect_area(left[0], left[1])
		right_area := rect_area(right[0], right[1])
		return left_area > right_area
	})
	return out
}

func is_rect_filled(c1, c2 Coord, filled matrix.Matrix) bool {
	x1, y1 := c1.Unpack()
	x2, y2 := c2.Unpack()
	for _, x := range my_range(x1, x2) {
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

func get_filled_squares(coords []Coord) matrix.Matrix {
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

type Edge [2]Coord

func get_unique_edges(arr []Coord) set.Set[Edge] {
	utils.Print("Got %v", arr)
	seen := set.Set[Edge]{}
	for _, left := range arr {
		for _, right := range arr {
			if left != right {
				l, r := order_coords(left, right)
				edge := Edge{l, r}
				seen.Add(edge)
			}
		}
	}
	return seen
}

// Order by smallest X coord, then smallest Y coord if X is equal.
func order_coords(a, b Coord) (Coord, Coord) {
	if a[0] < b[0] {
		return a, b
	} else if b[0] < a[0] {
		return b, a
	} else {
		if a[1] <= b[1] {
			return a, b
		} else {
			return b, a
		}
	}
}
