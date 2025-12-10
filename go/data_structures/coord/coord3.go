package coord

import (
	"fmt"
)

type Coord3 [3]int

func (c Coord3) String() string {
	return fmt.Sprintf("(%v, %v, %v)", c[0], c[1], c[2])
}

var _ fmt.Stringer = (*Coord3)(nil)

func (c Coord3) Unpack() (int, int, int) {
	return c[0], c[1], c[2]
}

func (c Coord3) Dx(other Coord3) int {
	return other[0] - c[0]
}
func (c Coord3) AbsDx(other Coord3) int {
	return abs(c.Dx(other))
}
func (c Coord3) Dy(other Coord3) int {
	return other[1] - c[1]
}
func (c Coord3) AbsDy(other Coord3) int {
	return abs(c.Dy(other))
}
func (c Coord3) Dz(other Coord3) int {
	return other[2] - c[2]
}
func (c Coord3) AbsDz(other Coord3) int {
	return abs(c.Dz(other))
}
func (c Coord3) EuclidianDistance(other Coord3) float64 {
	dx := c.Dx(other)
	dy := c.Dy(other)
	dz := c.Dz(other)
	return sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
}
func (c Coord3) TaxiCabDistance(other Coord3) int {
	return c.Dx(other) + c.Dy(other) + c.Dz(other)
}
