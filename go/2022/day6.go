package _2022

import (
	"fmt"
)

func findMarker(input string, length int) int {
	for xpos := length; xpos < len(input); xpos++ {
		snippet := input[xpos-length : xpos]
		unique := map[rune]bool{}
		for _, char := range snippet {
			unique[char] = true
		}
		if len(unique) == length {
			return xpos
		}
	}
	return 0
}

func Day6Part1(input string) string {
	return fmt.Sprint(findMarker(input, 4))
}

func Day6Part2(input string) string {
	return fmt.Sprint(findMarker(input, 14))
}
