package utils

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMaxIntHappy(t *testing.T) {
	assert.Equal(t, Max([]int{1, 2, 3}), 3)
	assert.Equal(t, Max([]int{-1, -2, -3}), -1)
	assert.Equal(t, Max([]int{-1, 2, -3}), 2)
	assert.Equal(t, Max([]int{0}), 0)
	assert.Equal(t, Max([]int{1, 0, 0, 0, -1}), 1)
}

func TestMaxFloatHappy(t *testing.T) {
	assert.Equal(t, Max([]float64{4, 5, 7}), 7.0)
	assert.Equal(t, Max([]float64{4.0, 5.0, 7.0}), 7.0)
	assert.Equal(t, Max([]float64{-4.0, -5.0, -7.0}), -4.0)
	assert.Equal(t, Max([]float64{6.9, 4.20, -666.666}), 6.9)
	assert.Equal(t, Max([]float64{0.0}), 0.0)
}

func TestMaxEmptyArray(t *testing.T) {
	assert.Panics(t, func() { Max([]int{}) }, "Max of empty array should panic")
	assert.Panics(t, func() { Max([]float64{}) }, "Max of empty array should panic")
}

func TestMinIntHappy(t *testing.T) {
	assert.Equal(t, Min([]int{1, 2, 3}), 1)
	assert.Equal(t, Min([]int{-1, -2, -3}), -3)
	assert.Equal(t, Min([]int{-1, 2, -3}), -3)
	assert.Equal(t, Min([]int{0}), 0)
	assert.Equal(t, Min([]int{1, 0, 0, 0, -1}), -1)
}
func TestMinFloatHappy(t *testing.T) {
	assert.Equal(t, Min([]float64{4, 5, 7}), 4.0)
	assert.Equal(t, Min([]float64{4.0, 5.0, 7.0}), 4.0)
	assert.Equal(t, Min([]float64{-4.0, -5.0, -7.0}), -7.0)
	assert.Equal(t, Min([]float64{6.9, 4.20, -666.666}), -666.666)
	assert.Equal(t, Min([]float64{0.0}), 0.0)
}

func TestMinEmptyArray(t *testing.T) {
	assert.Panics(t, func() { Min([]int{}) }, "Min of empty array should panic")
	assert.Panics(t, func() { Min([]float64{}) }, "Min of empty array should panic")
}

func TestSumIntHappy(t *testing.T) {
	assert.Equal(t, Sum([]int{1, 2, 3}), 6)
	assert.Equal(t, Sum([]int{1}), 1)
	assert.Equal(t, Sum([]int{5}), 5)
	assert.Equal(t, Sum([]int{-5}), -5)
	assert.Equal(t, Sum([]int{5, -5}), 0)
	assert.Equal(t, Sum([]int{0, 0}), 0)
	assert.Equal(t, Sum([]int{}), 0)
}

func TestSumFloatHappy(t *testing.T) {
	assert.Equal(t, Sum([]float64{1, 2, 3}), 6.0)
	assert.Equal(t, Sum([]float64{1}), 1.0)
	assert.Equal(t, Sum([]float64{5}), 5.0)
	assert.Equal(t, Sum([]float64{-5}), -5.0)
	assert.Equal(t, Sum([]float64{5, -5}), 0.0)
	assert.Equal(t, Sum([]float64{0.0}), 0.0)
	assert.Equal(t, Sum([]float64{}), 0.0)
}
