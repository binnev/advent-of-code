package _2015

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDay2Part1(t *testing.T) {
	assert.Equal(t, 58, calculate_wrapping_paper(2, 3, 4))
	assert.Equal(t, 43, calculate_wrapping_paper(1, 1, 10))
}
