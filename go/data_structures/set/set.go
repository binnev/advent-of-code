package set

import "fmt"

type Set[T comparable] map[T]bool

func (set Set[T]) Contains(key T) bool {
	_, ok := set[key]
	return ok
}

func (set *Set[T]) Add(values ...T) {
	for _, val := range values {
		(*set)[val] = true
	}
}

func (set *Set[T]) Remove(values ...T) {
	for _, val := range values {
		_, ok := (*set)[val]
		if !ok {
			panic(fmt.Sprintf("Value %v is not in set %v", val, set))
		}
		delete(*set, val)
	}
}

func FromString(s string) Set[rune] {
	set := Set[rune]{}
	for _, char := range s {
		set[char] = true
	}
	return set
}
func FromSlice[T comparable](arr []T) Set[T] {
	set := Set[T]{}
	for _, val := range arr {
		set[val] = true
	}
	return set
}
func (set Set[T]) ToSlice() []T {
	out := make([]T, len(set))
	for val := range set {
		out = append(out, val)
	}
	return out
}
