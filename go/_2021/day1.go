package _2021

import (
	"fmt"
	"strconv"
	"strings"

	"advent/utils"
)

func parseInput() []int {
	data := utils.LoadPuzzleInput("2021/day1")
	input_strings := strings.Fields(data)
	integers := make([]int, len(input_strings))
	for ind, str := range input_strings {
		i, _ := strconv.Atoi(str)
		integers[ind] = i
	}
	return integers
}

func Day1Part1() string {
	integers := parseInput()
	increases := 0
	previousDepth := 0
	for ii, depth := range integers {
		if ii == 0 {
			continue
		}
		if depth > previousDepth {
			increases++
		}
		previousDepth = depth
	}
	return fmt.Sprint(increases)
}

func Day1Part2() string {
	integers := parseInput()
	increases := 0
	windowWidth := 3
	previous := integers[0] + integers[1] + integers[2]
	for ii := windowWidth + 1; ii < len(integers)+1; ii++ {
		sum := 0
		for _, value := range integers[ii-windowWidth : ii] {
			sum += value
		}
		if sum > previous {
			increases++
		}
		previous = sum
	}
	return fmt.Sprint(increases)
}

func Day1() {
	utils.Profile(Day1Part1)
	utils.Profile(Day1Part2)
}
