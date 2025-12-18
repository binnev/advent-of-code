package set

import (
	"slices"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBasic(t *testing.T) {
	set := Set[int]{}
	assert.Equal(t, 0, len(set))

	set.Add(69)
	assert.Equal(t, 1, len(set))

	assert.False(t, set.Contains(420))
	assert.True(t, set.Contains(69))

	set.Remove(69)
	assert.False(t, set.Contains(69))

	// Trying to remove an item that's not in the set is fine -- this gives us
	// idempotent behaviour
	set.Remove(420)
}

func TestFromString(t *testing.T) {
	input := "string"
	set := FromString(input)
	for _, char := range input {
		assert.True(t, set.Contains(char))
	}
	assert.False(t, set.Contains('x'))
}

func TestFromSlice(t *testing.T) {
	input := []int{1, 2, 3}
	set := FromSlice(input)
	for _, val := range input {
		assert.True(t, set.Contains(val))
	}
	assert.False(t, set.Contains(69))
}

func TestCollect(t *testing.T) {
	it := slices.Values([]int{1, 2, 3})
	set := Collect(it)
	assert.Equal(t, FromSlice([]int{1, 2, 3}), set)
}

func TestAddManyFromSlice(t *testing.T) {
	set := Set[int]{}
	ints := []int{1, 2}
	set.Add(ints...)
	assert.True(t, set.Contains(1))
	assert.True(t, set.Contains(2))
}

func TestUpdate(t *testing.T) {
	set := Set[int]{}
	other := FromSlice([]int{1, 2})
	set.Update(other)
	assert.True(t, set.Contains(1))
	assert.True(t, set.Contains(2))
}

func TestAddSeq(t *testing.T) {
	ints := []int{1, 2}
	s := Set[int]{}
	s.AddSeq(slices.Values(ints))
	assert.Equal(t, 2, len(s))
}

func TestRemoveSeq(t *testing.T) {
	s := Set[int]{}
	ints := []int{1, 2}
	s.AddSeq(slices.Values(ints))
	assert.Equal(t, 2, len(s))
}

func TestValues(t *testing.T) {
	s := Set[int]{}
	s.Add(1, 2)
	assert.Equal(t, 2, len(s))

	// Remove values that are present
	s.RemoveSeq(slices.Values([]int{1, 2}))
	assert.Equal(t, 0, len(s))

	// Remove values that are not present
	s.RemoveSeq(slices.Values([]int{69, 420}))
}

func TestUnion(t *testing.T) {
	left := FromSlice([]int{1, 2})
	right := FromSlice([]int{2, 3, 4})
	expected := FromSlice([]int{1, 2, 3, 4})

	new := left.Union(right)

	assert.Equal(t, expected, new)
	assert.Equal(t, FromSlice([]int{1, 2}), left, "left should be unchanged")
	assert.Equal(t, FromSlice([]int{2, 3, 4}), right, "right should be unchanged")
}
