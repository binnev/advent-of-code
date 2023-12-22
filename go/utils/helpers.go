package utils

import (
	"strconv"
)

func ParseInt(s string) int {
	output, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return output
}

