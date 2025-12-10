package coord

import "math"

func abs(x int) int {
	return int(math.Abs(float64(x)))
}
func pow(x, exp int) int {
	return int(math.Pow(float64(x), float64(exp)))
}
func sqrt(x int) float64 {
	return math.Sqrt(float64(x))
}
