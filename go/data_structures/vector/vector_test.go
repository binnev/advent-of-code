package vector

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestInstantiation(t *testing.T) {
	// declare type and instantiate with curly braces
	_ = Vector[int]{420, 69, 9000, 666}

	// coerce from slice
	_ = Vector[int]([]int{1, 2, 3})
}

func TestLength(t *testing.T) {
	assert.Equal(t, 0, Vector[int]{}.Length())
	assert.Equal(t, 1, Vector[int]{420}.Length())
	assert.Equal(t, 2, Vector[int]{420, 69}.Length())
}

func TestFilter(t *testing.T) {
	t.Run("integers", func(t *testing.T) {

		vec := Vector[int]{420, 69, 9000, 666}
		assert.Equal(t,
			Vector[int]{},
			Vector[int]{}.Filter(func(i int) bool { return i > 500 }),
		)
		assert.Equal(t,
			Vector[int]{9000, 666},
			vec.Filter(func(i int) bool { return i > 500 }),
		)
		assert.Equal(t,
			Vector[int]{420, 9000, 666},
			vec.Filter(func(i int) bool { return i%2 == 0 }),
		)
	})

	t.Run("strings", func(t *testing.T) {
		strs := Vector[string]{"a", "dddd", "bb", "ccc"}
		assert.Equal(t,
			Vector[string]{"dddd", "ccc"},
			strs.Filter(func(s string) bool { return len(s) > 2 }),
		)
	})
}

func TestChainMethods(t *testing.T) {
	vec := Vector[int]{420, 69, 9000, 666}
	result := vec.Filter(func(i int) bool { return i > 100 }).Sort().Reverse()
	assert.Equal(t,
		Vector[int]{9000, 666, 420},
		result,
	)
}

func TestReduce(t *testing.T) {
	t.Run("integers", func(t *testing.T) {
		vec := Vector[int]{420, 69, 9000, 666}
		assert.Equal(t,
			vec.Reduce(func(a, b int) int { return a + b }),
			420+69+9000+666,
		)
		assert.Equal(t,
			vec.Reduce(func(a, b int) int { return a * b }),
			420*69*9000*666,
		)
		assert.Equal(t,
			vec.Reduce(func(a, b int) int { return a - b }),
			420-69-9000-666,
		)
	})
	t.Run("strings", func(t *testing.T) {
		vec := Vector[string]{"hello", "world"}
		assert.Equal(t,
			vec.Reduce(func(s1, s2 string) string { return s1 + s2 }),
			"helloworld",
		)
		assert.Equal(t,
			vec.Reduce(func(s1, s2 string) string { return s1[:3] + s2[:3] }),
			"helwor",
		)
	})
}
