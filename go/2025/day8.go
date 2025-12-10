package _2025

import (
	. "advent/data_structures/coord"
	"advent/data_structures/set"
	"advent/utils"
	"fmt"
	"maps"
	"math"
	"math/rand/v2"
	"slices"
	"sort"
	"strconv"
	"strings"
)

func Day8Part1(input string) string {
	result := get_product_top3_circuits(input, 1000)
	return fmt.Sprint(result)
}
func Day8Part2(input string) string {
	boxes := parse_day8(input)
	final_pair := make_circuits_until_all_connected(boxes)
	result := final_pair[0][0] * final_pair[1][0]
	return fmt.Sprint(result)
}

// Return the pair which causes all of the junction boxes to form a single
// circuit
func make_circuits_until_all_connected(boxes set.Set[Coord3]) Pair {
	distances := calc_distances(boxes)
	circuits := make(Circuits, len(boxes))

	// Explicitly add all the boxes to the circuits map, so that they are
	// considered for connectivity
	for box := range boxes {
		circuits[box] = 0
	}
	for n, pair := range distances.Closest() {
		circuits.Connect(pair)
		n_circuits := circuits.NumCircuits()
		if n_circuits == 1 {
			utils.Print("Finished after %v connections", n)
			return pair
		}
	}
	panic("Unreachable!")
}

func get_product_top3_circuits(input string, n_connections int) int {
	boxes := parse_day8(input)
	distances := calc_distances(boxes)
	circuits := make(Circuits, len(boxes))
	utils.Print("input = %v", input)
	utils.Print("boxes = %v", boxes)
	// utils.Print("distances = %v", distances)
	utils.Print("circuits = %v", circuits)
	for _, pair := range distances.Closest()[:n_connections] {
		circuits.Connect(pair)
	}
	largest_circuits := circuits.Largest()
	utils.Print("n_connections = %v", n_connections)
	utils.Print("largest_circuits = %v", largest_circuits)
	top3 := largest_circuits[:3]
	result := utils.Reduce(func(a, b int) int { return a * b }, top3)
	return result
}

func parse_day8(input string) set.Set[Coord3] {
	s := set.Set[Coord3]{}
	for line := range strings.Lines(input) {
		line = strings.TrimSpace(line)
		parts := strings.Split(line, ",")
		x, _ := strconv.Atoi(parts[0])
		y, _ := strconv.Atoi(parts[1])
		z, _ := strconv.Atoi(parts[2])
		coord := Coord3{x, y, z}
		s.Add(coord)
	}
	return s
}

// Map of Coord3: circuit number. If a coord is not in the map, it is not in a
// circuit.
type Circuits map[Coord3]int

func (ptr *Circuits) Connect(pair Pair) {
	circuits := *ptr
	left := pair[0]
	right := pair[1]

	left_circuit := circuits[left]
	right_circuit := circuits[right]

	// if neither is in a circuit, assign them both a new circuit
	if left_circuit == 0 && right_circuit == 0 {
		circuit_id := rand.Int64N(9999999999999)
		circuits[left] = int(circuit_id)
		circuits[right] = int(circuit_id)
	}

	// If one is in a circuit, add the other to it
	if left_circuit == 0 && right_circuit > 0 {
		circuits[left] = circuits[right]
	}
	if right_circuit == 0 && left_circuit > 0 {
		circuits[right] = circuits[left]
	}

	// If both are in separate circuits, assign all the coords from the right
	// circuit to the left circuit
	if left_circuit > 0 && right_circuit > 0 {
		for coord, circuit := range circuits {
			if circuit == right_circuit {
				circuits[coord] = left_circuit
			}
		}
	}
}
func (circuits Circuits) Largest() []int {
	circuit_ids := set.FromSlice(slices.Collect(maps.Values(circuits))).ToSlice()
	circuit_sizes := utils.Map(circuits.Count, circuit_ids)
	slices.Sort(circuit_sizes)
	slices.Reverse(circuit_sizes)
	return circuit_sizes
}

// Count the number of coords that are in the given circuit
func (circuits Circuits) Count(circuit int) int {
	total := 0
	for _, val := range circuits {
		if val == circuit {
			total++
		}
	}
	return total
}
func (circuits Circuits) NumCircuits() int {
	unique_circuit_ids := set.FromSlice(slices.Collect(maps.Values(circuits))).ToSlice()
	return len(unique_circuit_ids)
}

// Helper struct, mainly to handle ordering of Coord3 pairs
type Pair [2]Coord3 // ordered pair of coords
type DistanceMap map[Pair]float64

func (dm *DistanceMap) Add(a, b Coord3) {
	left, right := order_coords(a, b)
	dist := euclidian_distance(left, right)
	(*dm)[Pair{left, right}] = dist
}
func (dm DistanceMap) Get(a, b Coord3) float64 {
	left, right := order_coords(a, b)
	key := Pair{left, right}
	return dm[key]
}
func (dm DistanceMap) Closest() []Pair {
	keys := slices.Collect(maps.Keys(dm))
	sort.Slice(keys, func(i, j int) bool {
		return dm[keys[i]] < dm[keys[j]]
	})
	return keys
}

// Order by smallest X coord, then smallest Y coord if X is equal.
func order_coords(a, b Coord3) (Coord3, Coord3) {
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

func calc_distances(coords set.Set[Coord3]) DistanceMap {
	out := DistanceMap{}
	slice := coords.ToSlice()
	for _, left := range slice {
		for _, right := range slice {
			if left == right {
				continue // no distances to self
			}
			out.Add(left, right)
		}
	}
	return out
}

// sqrt(x**2 + y**2 + z**2)
func euclidian_distance(left, right Coord3) float64 {
	dx := left[0] - right[0]
	dy := left[1] - right[1]
	dz := left[2] - right[2]
	return math.Sqrt(
		math.Pow(float64(dx), 2) +
			math.Pow(float64(dy), 2) +
			math.Pow(float64(dz), 2),
	)
}
