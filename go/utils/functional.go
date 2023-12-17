package utils

import (
	"cmp"
	"sort"
)

func Map[I any, O any](f func(I) O, arr []I) []O {
	result := make([]O, len(arr))
	for ii, val := range arr {
		new_val := f(val)
		result[ii] = new_val
	}
	return result
}

func Filter[I any](f func(I) bool, arr []I) []I {
	result := []I{}
	for _, val := range arr {
		if f(val) {
			result = append(result, val)
		}
	}
	return result
}

func Reduce[I any](f func(I, I) I, arr []I) I {
	length := len(arr)
	if length < 2 {
		panic("can't reduce with <2 elements!")
	}
	result := f(arr[0], arr[1])
	for ii := 2; ii < length; ii++ {
		result = f(result, arr[ii])
	}
	return result
}

// Return the element of the slice that has the highest value according to the
// supplied getvalue function.
// Similar to python's `max(arr, key=getvalue)`
func Most[T any, O cmp.Ordered](getvalue func(T) O, slice []T) T {
	length := len(slice)
	if length == 0 {
		panic("Can't do comparisons on 0-length array!")
	}
	result := slice[0]
	greater := func(a, b T) bool {
		left := getvalue(a)
		right := getvalue(b)
		return left > right
	}
	for ii := 1; ii < length; ii++ {
		value := slice[ii]
		if greater(value, result) {
			result = value
		}
	}
	return result
}

func Least[T any, O cmp.Ordered](getvalue func(T) O, slice []T) T {
	length := len(slice)
	if length == 0 {
		panic("Can't do comparisons on 0-length array!")
	}
	result := slice[0]
	less := func(a, b T) bool {
		left := getvalue(a)
		right := getvalue(b)
		return left < right
	}
	for ii := 1; ii < length; ii++ {
		value := slice[ii]
		if less(value, result) {
			result = value
		}
	}
	return result
}

func Max[C cmp.Ordered](slice []C) C {
	big := func(c C) C { return c }
	return Most(big, slice)
}

func Min[C cmp.Ordered](slice []C) C {
	big := func(c C) C { return c }
	return Least(big, slice)
}

// Split an array into chunks of a given size.
// If the array does not evenly divide by the chunk_size,
// the last chunk will be truncated
// To use this with strings just pass in []byte(yourString)
func SplitArr[T any](arr []T, _chunk_size uint) [][]T {
	length := len(arr)

	// uint typing prevents passing negative numbers,
	// but we still need to check chunk_size is greater
	// than zero.
	chunk_size := int(_chunk_size)
	if chunk_size == 0 {
		panic("Chunk size must be > 0!")
	}

	// Make room for the truncated chunk if the array
	// doesn't evenly divide.
	count := length / chunk_size
	remainder := length % chunk_size
	if remainder > 0 {
		count++
	}
	result := make([][]T, count)

	for ii := 0; ii < count; ii++ {
		left := ii * chunk_size
		right := left + chunk_size
		if right > length {
			right = length
		}
		chunk := arr[left:right]
		result[ii] = chunk
	}
	return result
}

func Sum[T cmp.Ordered](arr []T) T {
	// if array is empty, return zero value
	// i.e. the sum of an empty array of ints is 0
	// i.e. the sum of an empty array of strings is ""
	var result T // initialises to empty value
	for _, value := range arr {
		result += value
	}
	return result
}

func copySlice[T any](arr []T) []T {
	cpy := make([]T, len(arr))
	copy(cpy, arr)
	return cpy
}

// Return a reversed copy of the slice
func Reverse[T cmp.Ordered](slice []T) []T {
	slice = copySlice(slice)
	sort.SliceStable(slice, func(i, j int) bool { return i > j })
	return slice
}

// Return a sorted (ascending) copy of the slice
func Sort[T cmp.Ordered](slice []T) []T {
	slice = copySlice(slice)
	sort.Slice(slice, func(i, j int) bool {
		// sort by comparing the values themselves
		left := slice[i]
		right := slice[j]
		return left < right
	})
	return slice
}

// Return a sorted copy of the slice, using the value function provided.
// This is like python's `sorted(arr, key=getvalue)`
func SortBy[T, O cmp.Ordered](slice []T, getvalue func(val T) O) []T {
	slice = copySlice(slice)
	sort.Slice(slice, func(i, j int) bool {
		// use the provided function to find values to compare
		left := getvalue(slice[i])
		right := getvalue(slice[j])
		return left < right
	})
	return slice
}

// Get the top N most common items in an array
// Return them in descending order
func TopN[T comparable](arr []T, N int) []T {
	// count frequency of each item
	counts := map[T]int{}
	for _, item := range arr {
		counts[item]++
	}
	// get unique values
	keys := []T{}
	for key := range counts {
		keys = append(keys, key)
	}
	// Sort descending
	sort.Slice(
		keys,
		func(i, j int) bool {
			left := keys[i]
			right := keys[j]
			return counts[left] > counts[right]
		},
	)
	return keys[:N]
}

func Contains[V int | string](arr []V, value V) bool {
	for _, item := range arr {
		if item == value {
			return true
		}
	}
	return false
}
