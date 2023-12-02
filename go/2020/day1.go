package _2020

import (
	"fmt"
	"strconv"
	"strings"
)

func parseInput(input string) []int {
	input_strings := strings.Fields(input)
	integers := make([]int, len(input_strings))
	for ind, str := range input_strings {
		i, _ := strconv.Atoi(str)
		integers[ind] = i
	}
	return integers
}

func Day1Part1(input string) string {
	integers := parseInput(input)
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

func Day1Part2(input string) string {
	integers := parseInput(input)
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
