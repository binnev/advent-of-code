package _2025

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const example_day5 = `3-5
10-14
16-20
12-18

1
5
8
11
17
32
`

func Test_Day5Part1(t *testing.T) {
	assert.Equal(t, "3", Day5Part1(example_day5))
}
