package _2022

import (
	"advent/utils"
	"fmt"
)

func findMarker(input string, length int) int {
	for xpos := length; xpos < len(input); xpos++ {
		snippet := input[xpos-length : xpos]
		unique := map[rune]int{}
		for _, char := range snippet {
			unique[char] = 0
		}
		if len(unique) == length {
			return xpos
		}
	}
	return 0
}

func Day6Part1() string {
	input := utils.LoadPuzzleInput("2022/day6")
	return fmt.Sprint(findMarker(input, 4))
}

func Day6Part2() string {
	input := utils.LoadPuzzleInput("2022/day6")
	return fmt.Sprint(findMarker(input, 14))
}

func Day6() {
	utils.Profile(Day6Part1)
	utils.Profile(Day6Part2)
}
