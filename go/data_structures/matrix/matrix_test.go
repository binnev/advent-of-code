package matrix

import (
	. "advent/data_structures/coord"
	"sort"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSparseMatrixXsYs(t *testing.T) {
	grid := Matrix{
		Coord{69, 420}:  '#',
		Coord{666, 888}: '#',
		Coord{777, 999}: '#',
	}
	xs := grid.xs()
	ys := grid.ys()
	sort.Ints(xs)
	sort.Ints(ys)
	assert.Equal(t, []int{69, 666, 777}, xs)
	assert.Equal(t, []int{420, 888, 999}, ys)
}

func TestSparseMatrixLimits(t *testing.T) {
	grid := Matrix{
		Coord{666, 888}:  '#',
		Coord{-69, -420}: '#',
		Coord{777, 999}:  '#',
	}
	min, max := grid.Xlim()
	assert.Equal(t, -69, min)
	assert.Equal(t, 777, max)

	min, max = grid.Ylim()
	assert.Equal(t, -420, min)
	assert.Equal(t, 999, max)
}

func TestSparseMatrixToString(t *testing.T) {
	type TestCase struct {
		description string
		grid        Matrix
		flipY       bool
		pad         int
		emptyChar   rune
		expected    string
	}
	cases := []TestCase{
		{
			description: "Empty default behaviour",
			grid:        Matrix{},
			flipY:       false,
			pad:         0,
			emptyChar:   '.',
			expected:    ".",
		},
		{
			description: "Empty with flip",
			grid:        Matrix{},
			flipY:       true,
			pad:         0,
			emptyChar:   '.',
			expected:    ".",
		},
		{
			description: "Empty with pad",
			grid:        Matrix{},
			flipY:       false,
			pad:         1,
			emptyChar:   '.',
			expected: strings.Join([]string{
				"...",
				"...",
				"...",
			}, "\n"),
		},
		{
			description: "Empty with pad and flip",
			grid:        Matrix{},
			flipY:       true,
			pad:         1,
			emptyChar:   '.',
			expected: strings.Join([]string{
				"...",
				"...",
				"...",
			}, "\n"),
		},
		{
			description: "Single entry default behaviour",
			grid:        Matrix{Coord{0, 0}: 'A'},
			flipY:       false,
			pad:         0,
			emptyChar:   '.',
			expected:    "A",
		},
		{
			description: "Single entry with flip",
			grid:        Matrix{Coord{0, 0}: 'A'},
			flipY:       true,
			pad:         0,
			emptyChar:   '.',
			expected:    "A",
		},
		{
			description: "Single entry with pad",
			grid:        Matrix{Coord{0, 0}: 'A'},
			flipY:       false,
			pad:         1,
			emptyChar:   '.',
			expected: strings.Join([]string{
				"...",
				".A.",
				"...",
			}, "\n"),
		},
		{
			description: "Single entry with pad and flip",
			grid:        Matrix{Coord{0, 0}: 'A'},
			flipY:       true,
			pad:         1,
			emptyChar:   '.',
			expected: strings.Join([]string{
				"...",
				".A.",
				"...",
			}, "\n"),
		},
		{
			description: "Non-empty default behaviour",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{2, 3}: 'B',
			},
			flipY:     false,
			pad:       0,
			emptyChar: '.',
			expected: strings.Join([]string{
				"A..",
				"...",
				"...",
				"..B",
			}, "\n"),
		},
		{
			description: "Non-empty with flip",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{2, 3}: 'B',
			},
			flipY:     true,
			pad:       0,
			emptyChar: '.',
			expected: strings.Join([]string{
				"..B",
				"...",
				"...",
				"A..",
			}, "\n"),
		},
		{
			description: "Non-empty with pad",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{2, 3}: 'B',
			},
			flipY:     false,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".......",
				".......",
				"..A....",
				".......",
				".......",
				"....B..",
				".......",
				".......",
			}, "\n"),
		},
		{
			description: "Non-empty with pad and flip",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{2, 3}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".......",
				".......",
				"....B..",
				".......",
				".......",
				"..A....",
				".......",
				".......",
			}, "\n"),
		},
		{
			description: "tall 6",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{0, 6}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".....",
				".....",
				"..B..",
				".....",
				".....",
				".....",
				".....",
				".....",
				"..A..",
				".....",
				".....",
			}, "\n"),
		},
		{
			description: "tall 7",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{0, 7}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".....",
				".....",
				"..B..",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				"..A..",
				".....",
				".....",
			}, "\n"),
		},
		{
			description: "tall 8",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{0, 8}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".....",
				".....",
				"..B..",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				"..A..",
				".....",
				".....",
			}, "\n"),
		},
		{
			description: "tall 9",
			grid: Matrix{
				Coord{0, 0}: 'A',
				Coord{0, 9}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".....",
				".....",
				"..B..",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				"..A..",
				".....",
				".....",
			}, "\n"),
		},
		{
			description: "tall 10",
			grid: Matrix{
				Coord{0, 0}:  'A',
				Coord{0, 10}: 'B',
			},
			flipY:     true,
			pad:       2,
			emptyChar: '.',
			expected: strings.Join([]string{
				".....",
				".....",
				"..B..",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				".....",
				"..A..",
				".....",
				".....",
			}, "\n"),
		},
	}
	for _, tc := range cases {
		t.Run(tc.description, func(t *testing.T) {
			result := tc.grid.ToString(
				tc.flipY,
				tc.pad,
				tc.emptyChar,
			)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func TestSparseMatrixConstruct(t *testing.T) {
	EXPECTED := strings.Join([]string{
		"......#.....",
		"..........#.",
		".#.#..#.....",
		".....#......",
		"..#.....#..#",
		"#......##...",
		"....##......",
		".#........#.",
		"...#.#..#...",
		"............",
		"...#..#..#..",
	}, "\n")

	t.Run("no ignore", func(t *testing.T) {
		grid := Matrix{}.FromString(EXPECTED, "")
		assert.Equal(t, 12*11, len(grid), "all characters should be read in")
		assert.Equal(t, EXPECTED, grid.ToString(false, 0, '.'))
	})
	t.Run("with ignore", func(t *testing.T) {
		grid := Matrix{}.FromString(EXPECTED, ".")
		assert.Equal(t, 22, len(grid), "only #s should be read in")
		assert.Equal(t, EXPECTED, grid.ToString(false, 0, '.'))
	})
}
