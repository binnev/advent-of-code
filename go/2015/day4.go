package _2015

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
)

const LIMIT = 10_000_000

func Day4Part1(input string) string {
	return find_hash_with_n_leading_zeroes(input, 5)
}

func Day4Part2(input string) string {
	return find_hash_with_n_leading_zeroes(input, 6)
}

func find_hash_with_n_leading_zeroes(input string, n int) string {
	for ii := 0; ii < LIMIT; ii++ {
		hash := _md5(input, ii)
		if starts_with_n_zeroes(hash, n) {
			return fmt.Sprint(ii)
		}
	}
	panic("Reached search limit!")
}

func _md5(secret_key string, number int) string {
	hasher := md5.New()
	s := fmt.Sprintf("%v%v", secret_key, number)
	io.WriteString(hasher, s)
	return hex.EncodeToString(hasher.Sum(nil))
}

func starts_with_n_zeroes(s string, n int) bool {
	for ii, ch := range s {
		if ch != '0' {
			return false
		}
		if ii >= n-1 {
			return true
		}
	}
	return false
}
