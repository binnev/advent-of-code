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
	level := 0
	for position, ch := range input {
		if ch == '(' {
			level++
		}
		if ch == ')' {
			level--
		}
		if level < 0 {
			return fmt.Sprint(position + 1)
		}
	}
	return ""
}
