package utils

import (
	"fmt"
	"strconv"
)

func ParseInt(s string) int {
	output, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return output
}

func Print(s string, args ...any) {
	fmt.Println(fmt.Sprintf(s, args...))
}
