package coord

import (
	"fmt"
)

type Coord3 struct{ x, y, z int }

func (c Coord3) String() string {
	return fmt.Sprintf("(%v, %v, %v)", c.x, c.y, c.z)
}

var _ fmt.Stringer = (*Coord3)(nil)

func (c Coord3) Unpack() (int, int, int) {
	return c.x, c.y, c.z
}

func (c Coord3) Dx(other Coord3) int {
	return other.x - c.x
}
func (c Coord3) AbsDx(other Coord3) int {
	return abs(c.Dx(other))
}
func (c Coord3) Dy(other Coord3) int {
	return other.y - c.y
}
func (c Coord3) AbsDy(other Coord3) int {
	return abs(c.Dy(other))
}
func (c Coord3) Dz(other Coord3) int {
	return other.z - c.z
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
