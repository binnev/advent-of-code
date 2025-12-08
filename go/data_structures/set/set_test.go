package set

import (
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

	// Can't remove an item that's not in the set
	assert.Panics(t, func() { set.Remove(420) })
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
