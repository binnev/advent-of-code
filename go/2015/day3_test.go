package _2015

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_Day3Part1(t *testing.T) {
	assert.Equal(t, "2", Day3Part1("^v"))
	assert.Equal(t, "4", Day3Part1("^>v<"))
	assert.Equal(t, "2", Day3Part1("^v^v^v^v^v"))
}

func Test_Day3Part2(t *testing.T) {
	assert.Equal(t, "3", Day3Part2("^v"))
	assert.Equal(t, "3", Day3Part2("^>v<"))
	assert.Equal(t, "11", Day3Part2("^v^v^v^v^v"))
}
