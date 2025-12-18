package set

import (
	"advent/utils"
	"fmt"
	"iter"
	"maps"
	"slices"
	"strings"
)

type Set[T comparable] map[T]bool

func (s Set[T]) Contains(key T) bool {
	_, ok := s[key]
	return ok
}

func (s *Set[T]) Add(values ...T) {
	for _, val := range values {
		(*s)[val] = true
	}
}

// NOTE: doesn't panic if the value is not present
func (s *Set[T]) Remove(values ...T) {
	for _, val := range values {
		delete(*s, val)
	}
}

// Merge this set with another and return the result without modifying the
// original.
func (s Set[T]) Union(other Set[T]) Set[T] {
	// So much for value receivers not mutating the original... apparently maps
	// and slices are exempt from this rule because they are rEfErEnCe TyPeS
	new := Set[T]{}
	maps.Copy(new, s)

	for item := range other {
		new.Add(item)
	}
	return new
}

// Merge another set into this set in place
func (s Set[T]) Update(other Set[T]) {
	for item := range other {
		s.Add(item)
	}
}

func FromSlice[T comparable](arr []T) Set[T] {
	return Collect(slices.Values(arr))
}
func (s Set[T]) ToSlice() []T {
	return slices.Collect(s.Values())
}

// =============================== string stuff ================================

func (s Set[T]) String() string {
	out := "{"
	slice := slices.Collect(maps.Keys(s))
	f := func(a T) string { return fmt.Sprint(a) }
	out += strings.Join(utils.Map(f, slice), ", ")
	out += "}"
	return out
}

var _ fmt.Stringer = (*Set[any])(nil)

func FromString(s string) Set[rune] {
	set := Set[rune]{}
	for _, char := range s {
		set[char] = true
	}
	return set
}

// ================================= iter stuff ================================

func Collect[T comparable](seq iter.Seq[T]) Set[T] {
	s := Set[T]{}
	for item := range seq {
		s.Add(item)
	}
	return s
}

func (s Set[T]) Values() iter.Seq[T] {
	return func(yield func(T) bool) {
		for item := range s {
			if !yield(item) {
				return
			}
		}
	}
}

func (s *Set[T]) AddSeq(seq iter.Seq[T]) {
	for val := range seq {
		s.Add(val)
	}
}

func (s *Set[T]) RemoveSeq(seq iter.Seq[T]) {
	for val := range seq {
		s.Remove(val)
	}
}
