package vector

import (
	"advent/utils"
	"cmp"
)

type Vector[T cmp.Ordered] []T

func (v Vector[T]) Filter(f func(T) bool) Vector[T] {
	slice := utils.Filter(f, v)
	return Vector[T](slice)
}

func (v Vector[T]) Reduce(f func(T, T) T) T {
	return utils.Reduce(f, v)
}

func (v Vector[T]) Length() int {
	return len(v)
}

func (v Vector[T]) Sort() Vector[T] {
	slice := utils.Sort(v)
	return Vector[T](slice)
}

func (v Vector[T]) Reverse() Vector[T] {
	slice := utils.Reverse(v)
	return Vector[T](slice)
}

func (v Vector[T]) Contains(needle T) bool {
	return utils.Contains(v, needle)
}

func (v Vector[T]) TopN(n int) Vector[T] {
	slice := utils.TopN(v, n)
	return Vector[T](slice)
}
