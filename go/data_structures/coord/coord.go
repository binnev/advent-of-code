package coord

import (
	"fmt"
)

type Coord [2]int

func (c Coord) String() string {
	return fmt.Sprintf("(%v, %v)", c[0], c[1])
}

var _ fmt.Stringer = (*Coord)(nil)

// Easy unpacking x, y := coord.Unpack()
func (c Coord) Unpack() (int, int) {
	return c[0], c[1]
}

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
