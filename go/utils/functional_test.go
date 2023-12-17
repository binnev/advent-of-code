package utils

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMap(t *testing.T) {
	arr := []int{1, 2, 3}

	stringify := func(i int) string { return fmt.Sprintf("%v", i) }
	assert.Equal(t, []string{"1", "2", "3"}, Map(stringify, arr))

	double := func(i int) int { return i * 2 }
	assert.Equal(t, []int{2, 4, 6}, Map(double, arr))
}

func TestFilter(t *testing.T) {
	arr := []int{1, 2, 3}
	strings := []string{"a", "bbbb", "cccccccc"}

	isOdd := func(i int) bool { return i%2 != 0 }
	assert.Equal(t, []int{1, 3}, Filter(isOdd, arr))

	greaterThan2 := func(i int) bool { return i > 2 }
	assert.Equal(t, []int{3}, Filter(greaterThan2, arr))

	longerThan4 := func(s string) bool { return len(s) > 4 }
	assert.Equal(t, []string{"cccccccc"}, Filter(longerThan4, strings))
}

func TestReduce(t *testing.T) {
	arr := []int{1, 2, 3}
	strings := []string{"Oh", "hi", "Mark"}

	sum := func(a, b int) int { return a + b }
	assert.Equal(t, 6, Reduce(sum, arr))

	product := func(a, b int) int { return a * b }
	assert.Equal(t, 6, Reduce(product, arr))

	cat := func(a, b string) string { return a + b }
	assert.Equal(t, "OhhiMark", Reduce(cat, strings))
}

func TestMax(t *testing.T) {
	assert.Equal(t, 3, Max([]int{3, 2, 1}))
	assert.Equal(t, 4.0, Max([]float64{3.4, 2.1, 4.0, 1.1}))
	assert.Equal(t, "zzz", Max([]string{"a", "b", "zzz"}))
	assert.Equal(t, Max([]int{1, 2, 3}), 3)
	assert.Equal(t, Max([]int{-1, -2, -3}), -1)
	assert.Equal(t, Max([]int{-1, 2, -3}), 2)
	assert.Equal(t, Max([]int{0}), 0)
	assert.Equal(t, Max([]int{1, 0, 0, 0, -1}), 1)
	assert.Equal(t, Max([]int{0, 0, 1000, 0, -1000}), 1000)
	assert.Equal(t, Max([]float64{4, 5, 7}), 7.0)
	assert.Equal(t, Max([]float64{4.0, 5.0, 7.0}), 7.0)
	assert.Equal(t, Max([]float64{-4.0, -5.0, -7.0}), -4.0)
	assert.Equal(t, Max([]float64{6.9, 4.20, -666.666}), 6.9)
	assert.Equal(t, Max([]float64{0.0}), 0.0)
	assert.Panics(t, func() { Max([]int{}) }, "Max of empty array should panic")
	assert.Panics(t, func() { Max([]float64{}) }, "Max of empty array should panic")
}

func TestMin(t *testing.T) {
	assert.Equal(t, 1, Min([]int{1, 2, 3}))
	assert.Equal(t, 1.1, Min([]float64{1.1, 2.2, 3.3, 4.4}))
	assert.Equal(t, "a", Min([]string{"a", "b", "zzz"}))
	assert.Equal(t, Min([]int{1, 2, 3}), 1)
	assert.Equal(t, Min([]int{-1, -2, -3}), -3)
	assert.Equal(t, Min([]int{-1, 2, -3}), -3)
	assert.Equal(t, Min([]int{0}), 0)
	assert.Equal(t, Min([]int{1, 0, 0, 0, -1}), -1)
	assert.Equal(t, Min([]int{0, 0, 1000, 0, -1000}), -1000)
	assert.Equal(t, Min([]float64{4, 5, 7}), 4.0)
	assert.Equal(t, Min([]float64{4.0, 5.0, 7.0}), 4.0)
	assert.Equal(t, Min([]float64{-4.0, -5.0, -7.0}), -7.0)
	assert.Equal(t, Min([]float64{6.9, 4.20, -666.666}), -666.666)
	assert.Equal(t, Min([]float64{0.0}), 0.0)
	assert.Panics(t, func() { Min([]int{}) }, "Min of empty array should panic")
	assert.Panics(t, func() { Min([]float64{}) }, "Min of empty array should panic")
}

func TestSplitArr(t *testing.T) {
	type TestCase struct {
		description  string
		input_arr    []any
		chunk_size   uint
		expected_out [][]any
	}
	cases := []TestCase{
		{
			description:  "1-length chunks",
			input_arr:    []any{1, 2, 3},
			chunk_size:   1,
			expected_out: [][]any{{1}, {2}, {3}},
		},
		{
			description:  "2-length chunks",
			input_arr:    []any{1, 2, 3, 4},
			chunk_size:   2,
			expected_out: [][]any{{1, 2}, {3, 4}},
		},
		{
			description:  "chunk size == array length",
			input_arr:    []any{1, 2, 3},
			chunk_size:   3,
			expected_out: [][]any{{1, 2, 3}},
		},
		{
			description:  "divides evenly",
			input_arr:    []any{1, 2, 3, 4, 5, 6, 7, 8, 9},
			chunk_size:   3,
			expected_out: [][]any{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}},
		},
		{
			description:  "final chunk is truncated",
			input_arr:    []any{1, 2, 3, 4, 5, 6, 7, 8, 9},
			chunk_size:   4,
			expected_out: [][]any{{1, 2, 3, 4}, {5, 6, 7, 8}, {9}},
		},
		{
			description:  "final chunk is truncated",
			input_arr:    []any{1, 2, 3, 4, 5, 6, 7, 8, 9},
			chunk_size:   5,
			expected_out: [][]any{{1, 2, 3, 4, 5}, {6, 7, 8, 9}},
		},
		{
			description:  "works on float64",
			input_arr:    []any{1.1, 2.2, 3.3, 4.4},
			chunk_size:   2,
			expected_out: [][]any{{1.1, 2.2}, {3.3, 4.4}},
		},
	}
	for _, testcase := range cases {
		t.Run(testcase.description, func(t *testing.T) {
			result := SplitArr(testcase.input_arr, testcase.chunk_size)
			assert.Equal(t, testcase.expected_out, result)
		})
	}
}

func TestSplitArrWithString(t *testing.T) {
	input := "Hello, world!"
	result := SplitArr([]byte(input), 2)
	assert.Equal(t,
		[][]byte{
			[]byte("He"),
			[]byte("ll"),
			[]byte("o,"),
			[]byte(" w"),
			[]byte("or"),
			[]byte("ld"),
			[]byte("!"),
		},
		result,
	)
}

func TestSum(t *testing.T) {
	t.Run("ints", func(t *testing.T) {
		assert.Equal(t, 6, Sum([]int{1, 2, 3}))
		assert.Equal(t, 0, Sum([]int{}))
		assert.Equal(t, Sum([]int{1, 2, 3}), 6)
		assert.Equal(t, Sum([]int{1}), 1)
		assert.Equal(t, Sum([]int{5}), 5)
		assert.Equal(t, Sum([]int{-5}), -5)
		assert.Equal(t, Sum([]int{5, -5}), 0)
		assert.Equal(t, Sum([]int{0, 0}), 0)
		assert.Equal(t, Sum([]int{}), 0)
	})
	t.Run("floats", func(t *testing.T) {
		assert.Equal(t, 6.6, Sum([]float64{1.1, 2.2, 3.3}))
		assert.Equal(t, 0.0, Sum([]float64{}))
		assert.Equal(t, Sum([]float64{1, 2, 3}), 6.0)
		assert.Equal(t, Sum([]float64{1}), 1.0)
		assert.Equal(t, Sum([]float64{5}), 5.0)
		assert.Equal(t, Sum([]float64{-5}), -5.0)
		assert.Equal(t, Sum([]float64{5, -5}), 0.0)
		assert.Equal(t, Sum([]float64{0.0}), 0.0)
		assert.Equal(t, Sum([]float64{}), 0.0)
	})
	t.Run("strings", func(t *testing.T) {
		assert.Equal(t, "abbccc", Sum([]string{"a", "bb", "ccc"}))
		assert.Equal(t, "", Sum([]string{}))
	})
}

func TestTopN(t *testing.T) {
	assert.Equal(
		t,
		[]int{1, 2, 6},
		TopN([]int{1, 1, 1, 1, 2, 2, 2, 6, 6, 5}, 3),
	)
}

func TestReverse(t *testing.T) {
	type TestCase struct {
		description string
		input       []string
		expected    []string
	}
	cases := []TestCase{
		{
			description: "empty",
			input:       []string{},
			expected:    []string{},
		},
		{
			description: "single entry",
			input:       []string{"a"},
			expected:    []string{"a"},
		},
		{
			description: "populated odd",
			input:       []string{"a", "b", "c"},
			expected:    []string{"c", "b", "a"},
		},
		{
			description: "populated even",
			input:       []string{"...", "aaa", "...", "bbb"},
			expected:    []string{"bbb", "...", "aaa", "..."},
		},
		{
			description: "short",
			input:       []string{"A", ".", "B"},
			expected:    []string{"B", ".", "A"},
		},
		{
			description: "medium",
			input:       []string{"A", ".", ".", "B"},
			expected:    []string{"B", ".", ".", "A"},
		},
		{
			description: "long",
			input:       []string{"A", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=9",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=10",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=11",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
		{
			description: "len=12",
			input:       []string{"A", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "B"},
			expected:    []string{"B", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "A"},
		},
	}
	for _, tc := range cases {
		t.Run(tc.description, func(t *testing.T) {
			reversed := Reverse(tc.input)
			assert.Equal(t, tc.expected, reversed)
		})
	}
}

func TestSort(t *testing.T) {
	t.Run("empty array", func(t *testing.T) {
		in := []int{}
		out := Sort(in)
		assert.Equal(t, []int{}, in) // should be unchanged
		assert.Equal(t, []int{}, out)
	})
	t.Run("strings", func(t *testing.T) {
		in := []string{"c", "b", "a"}
		out := Sort(in)
		assert.Equal(t, []string{"c", "b", "a"}, in) // should be unchanged
		assert.Equal(t, []string{"a", "b", "c"}, out)
	})
	t.Run("ints", func(t *testing.T) {
		in := []int{3, 2, 1}
		out := Sort(in)
		assert.Equal(t, []int{3, 2, 1}, in) // should be unchanged
		assert.Equal(t, []int{1, 2, 3}, out)
	})
	t.Run("floats", func(t *testing.T) {
		in := []float64{3.3, 2.2, 1.1}
		out := Sort(in)
		assert.Equal(t, []float64{3.3, 2.2, 1.1}, in) // should be unchanged
		assert.Equal(t, []float64{1.1, 2.2, 3.3}, out)
	})
}

func TestSortBy(t *testing.T) {
	t.Run("sorting map keys by map value", func(t *testing.T) {
		lengths := map[string]int{
			"hi":        2,
			"hello":     5,
			"greetings": 9,
		}
		keys := []string{"hi", "hello", "greetings", "bye"}
		sorted := SortBy(keys, func(s string) int {
			score, _ := lengths[s] // defaults to 0 if not present
			return score
		})
		assert.Equal(t, []string{"bye", "hi", "hello", "greetings"}, sorted)
	})
	t.Run("function that always returns the same thing should not sort", func(t *testing.T) {
		slice := []float64{2.2, 1.1, 3.3}
		sorted := SortBy(slice, func(f float64) int { return 0 })
		assert.Equal(t, []float64{2.2, 1.1, 3.3}, sorted)
	})
	t.Run("empty array", func(t *testing.T) {
		slice := []int{}
		sorted := SortBy(slice, func(i int) int { return 0 })
		assert.Equal(t, []int{}, sorted)
	})
}

func TestMost(t *testing.T) {
	t.Run("find the longest string", func(t *testing.T) {
		slice := []string{"a", "ccc", "bb"}
		long := func(a string) int { return len(a) }
		out := Most(long, slice)
		assert.Equal(t, "ccc", out)
	})
	t.Run("find the shortest string", func(t *testing.T) {
		slice := []string{"a", "ccc", "bb"}
		short := func(a string) int { return -len(a) }
		out := Most(short, slice)
		assert.Equal(t, "a", out)
	})
	t.Run("find the largest integer", func(t *testing.T) {
		slice := []int{1, 2, 3}
		big := func(a int) int { return a }
		out := Most(big, slice)
		assert.Equal(t, 3, out)
	})
	t.Run("find the smallest integer", func(t *testing.T) {
		slice := []int{1, 2, 3}
		small := func(a int) int { return -a }
		out := Most(small, slice)
		assert.Equal(t, 1, out)
	})
}

func TestLeast(t *testing.T) {
	t.Run("find the shortest string", func(t *testing.T) {
		slice := []string{"a", "ccc", "bb"}
		long := func(a string) int { return len(a) }
		out := Least(long, slice)
		assert.Equal(t, "a", out)
	})
	t.Run("find the longest string", func(t *testing.T) {
		slice := []string{"a", "ccc", "bb"}
		short := func(a string) int { return -len(a) }
		out := Least(short, slice)
		assert.Equal(t, "ccc", out)
	})
	t.Run("find the smallest integer", func(t *testing.T) {
		slice := []int{1, 2, 3}
		big := func(a int) int { return a }
		out := Least(big, slice)
		assert.Equal(t, 1, out)
	})
	t.Run("find the largest integer", func(t *testing.T) {
		slice := []int{1, 2, 3}
		small := func(a int) int { return -a }
		out := Least(small, slice)
		assert.Equal(t, 3, out)
	})
}

func TestContains(t *testing.T) {
	type TestCase struct {
		description string
		haystack    []int
		needle      int
		expected    bool
	}
	cases := []TestCase{
		{description: "happy", haystack: []int{1, 2, 3}, needle: 2, expected: true},
		{description: "sad", haystack: []int{1, 2, 3}, needle: 69, expected: false},
		{description: "empty", haystack: []int{}, needle: 69, expected: false},
	}
	for _, tc := range cases {
		t.Run(tc.description, func(t *testing.T) {
			result := Contains(tc.haystack, tc.needle)
			assert.Equal(t, tc.expected, result)
		})
	}
}
