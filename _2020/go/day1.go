package main

import (
	"fmt"
	"strconv"
	"strings"
	"utils"
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

func day1part1() string {
	integers := parseInput()
	value := 0
	for _, a := range integers {
		for _, b := range integers {
			if a+b == 2020 {
				value = a * b
				break
			}
		}
	}
	return fmt.Sprintf("%v", value)
}

func day1part2() string {
	integers := parseInput()
	value := 0
	for _, a := range integers {
		for _, b := range integers {
			for _, c := range integers {
				if a+b+c == 2020 {
					value = a * b * c
					break
				}
			}
		}
	}
	return fmt.Sprintf("%v", value)
}

func day1main() {
	utils.Profile(day1part1)
	utils.Profile(day1part2)
}
