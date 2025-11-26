package _2015

import (
	"fmt"
	"strings"
)

func Day1Part1(input string) string {
	up := strings.Count(input, "(")
	down := strings.Count(input, ")")
	result := up - down
	return fmt.Sprint(result)
}
func Day1Part2(input string) string {
	return ""
}
