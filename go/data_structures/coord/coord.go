package coord

import (
	"fmt"
	"math"
)

type Coord struct{ x, y int }

func (c Coord) String() string {
	return fmt.Sprintf("(%v, %v)", c.x, c.y)
}

var _ fmt.Stringer = (*Coord)(nil)

// Easy unpacking x, y := coord.Unpack()
func (c Coord) Unpack() (int, int) {
	return c.x, c.y
}

func (c Coord) Dx(other Coord) int {
	return other.x - c.x
}
func (c Coord) AbsDx(other Coord) int {
	return abs(c.Dx(other))
}
func (c Coord) Dy(other Coord) int {
	return other.y - c.y
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

func abs(x int) int {
	return int(math.Abs(float64(x)))
}
func pow(x, exp int) int {
	return int(math.Pow(float64(x), float64(exp)))
}
func sqrt(x int) float64 {
	return math.Sqrt(float64(x))
}
