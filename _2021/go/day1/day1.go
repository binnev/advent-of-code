package day1

import (
	"fmt"
	"strconv"
	"strings"

	"advent/utils"
)

func parseInput() []int {
	data := utils.LoadPuzzleInput("day1")
	input_strings := strings.Fields(data)
	integers := make([]int, len(input_strings))
	for ind, str := range input_strings {
		i, _ := strconv.Atoi(str)
		integers[ind] = i
	}
	return integers
}

func Part1() string {
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

func Part2() string {
	integers := parseInput()
	increases := 0
	for ii := 0; ii < len(integers)-4; ii++ {
		currentWindow := integers[ii : ii+3]
		nextWindow := integers[ii+1 : ii+4]
		sumNext := 0
		for _, value := range nextWindow {
			sumNext += value
		}
		sumCurrent := 0
		for _, value := range currentWindow {
			sumCurrent += value
		}
		if sumNext > sumCurrent {
			increases++
		}
	}
	return fmt.Sprint(increases)
}

func All() {
	utils.Profile(Part1)
	utils.Profile(Part2)
}
