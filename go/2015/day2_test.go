package _2015

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_calculate_wrapping_paper(t *testing.T) {
	assert.Equal(t, 58, calculate_wrapping_paper(2, 3, 4))
	assert.Equal(t, 43, calculate_wrapping_paper(1, 1, 10))
}

func Test_calculate_ribbon(t *testing.T) {
	assert.Equal(t, 34, calculate_ribbon(2, 3, 4))
	assert.Equal(t, 14, calculate_ribbon(1, 1, 10))
}
