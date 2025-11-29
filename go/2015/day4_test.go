package _2015

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_Day4Part1(t *testing.T) {
	// If your secret key is abcdef, the answer is 609043, because the MD5 hash
	// of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the
	// lowest such number to do so.
	assert.Equal(t, "609043", Day4Part1("abcdef"))

	// If your secret key is pqrstuv, the lowest number it combines with to make
	// an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash
	// of pqrstuv1048970 looks like 000006136ef....
	assert.Equal(t, "1048970", Day4Part1("pqrstuv"))
}

func Test__md5(t *testing.T) {
	hash := _md5("abcdef", 609043)
	assert.Equal(t, true, strings.Contains(hash, "000001dbbfa"))

	hash = _md5("pqrstuv", 1048970)
	assert.Equal(t, true, strings.Contains(hash, "000006136ef"))
}

func Test_starts_with_five_zeroes(t *testing.T) {
	assert.Equal(t, false, starts_with_n_zeroes("a", 5))
	assert.Equal(t, false, starts_with_n_zeroes("0000aaaa", 5))
	assert.Equal(t, true, starts_with_n_zeroes("00000aaaa", 5))
	assert.Equal(t, true, starts_with_n_zeroes("000000aaaa", 5))
	assert.Equal(t, true, starts_with_n_zeroes("000000aaaa", 6))
	assert.Equal(t, false, starts_with_n_zeroes("00000aaaa", 6))
}
