package coord

import (
	"advent/utils"
	"fmt"
	"strings"
)

type Coord [2]int

// Implementations of interfaces -----------------------------------------------
func (c Coord) String() string {
	return fmt.Sprintf("(%v, %v)", c[0], c[1])
}

var _ fmt.Stringer = (*Coord)(nil)

// Utils -----------------------------------------------------------------------
func (c Coord) Unpack() (int, int) {
	return c[0], c[1]
}
func (c Coord) FromString(s string) Coord {
	parts := strings.Split(s, ",")[:2]
	parts = utils.Map(strings.TrimSpace, parts)
	numbers := utils.Map(utils.ParseInt, parts)
	return Coord{numbers[0], numbers[1]}
}

// Return the neighbours in the 4 cardinal directions
func (c Coord) CardinalNeighbours() []Coord {
	x, y := c.Unpack()
	return []Coord{
		{x + 1, y},
		{x - 1, y},
		{x, y + 1},
		{x, y - 1},
	}
}

// Math stuff ------------------------------------------------------------------
func (c Coord) Dx(other Coord) int {
	return other[0] - c[0]
}
func (c Coord) AbsDx(other Coord) int {
	return abs(c.Dx(other))
}
func (c Coord) Dy(other Coord) int {
	return other[1] - c[1]
}
func (c Coord) AbsDy(other Coord) int {
	return abs(c.Dy(other))
}
func (c Coord) EuclidianDistance(other Coord) float64 {
	dx := c.Dx(other)
	dy := c.Dy(other)
	return sqrt(pow(dx, 2) + pow(dy, 2))
}
func (c Coord) TaxiCabDistance(other Coord) int {
	return c.Dx(other) + c.Dy(other)
}
