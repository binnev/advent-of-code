package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day4 = `..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.`

func TestDay4Part1(t *testing.T) {
	assert.Equal(t, "13", Day4Part1(example_day4))
}

func TestDay4Part2(t *testing.T) {
	assert.Equal(t, "43", Day4Part2(example_day4))
}
