package _2015

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
)

const LIMIT = 10_000_000

func Day4Part1(input string) string {
	for ii := 0; ii < LIMIT; ii++ {
		hash := _md5(input, ii)
		if starts_with_five_zeroes(hash) {
			return fmt.Sprint(ii)
		}
	}
	return ""
}

func Day4Part2(input string) string {
	return ""
}

func _md5(secret_key string, number int) string {
	hasher := md5.New()
	s := fmt.Sprintf("%v%v", secret_key, number)
	io.WriteString(hasher, s)
	return hex.EncodeToString(hasher.Sum(nil))
}

func starts_with_five_zeroes(s string) bool {
	for ii, ch := range s {
		if ch != '0' {
			return false
		}
		if ii >= 4 {
			return true
		}
	}
	return false
}
