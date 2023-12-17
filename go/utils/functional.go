package utils

import (
	"math"
	"strconv"
)

func ParseInt(s string) int {
	output, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return output
}

func Sum[V int | float64](arr []V) V {
	var sum V
	for _, item := range arr {
		sum += item
	}
	return sum
}

func Max[V int | float64](arr []V) V {
	if len(arr) == 0 {
		panic("Can't do max of empty array")
	}
	max := math.Inf(-1)
	for _, item := range arr {
		floated := float64(item)
		if floated > max {
			max = floated
		}
	}
	return V(max)
}

func Min[V int | float64](arr []V) V {
	if len(arr) == 0 {
		panic("Can't do min of empty array")
	}
	min := math.Inf(1)
	for _, item := range arr {
		floated := float64(item)
		if floated < min {
			min = floated
		}
	}
	return V(min)
}

func Contains[V int | string](arr []V, value V) bool {
	for _, item := range arr {
		if item == value {
			return true
		}
	}
	return false
}

func Reverse[AnySlice ~[]A, A any](arr AnySlice) {
	reversed := make(AnySlice, len(arr))
	length := len(arr)
	for ii, value := range arr {
		reversed[length-1-ii] = value
	}
	copy(arr, reversed)
}

func Map[I any, O any](f func(I) O, arr []I) []O {
	result := make([]O, len(arr))
	for ii, item := range arr {
		result[ii] = f(item)
	}
	return result
}
